from django.shortcuts import render, get_object_or_404, redirect
from app.balance.models import Balance
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.balance.forms import BalanceForm
from app.empresa.models import Empresa
from app.cuentaBalance.models import CuentaBalance
from django.core.paginator import Paginator

from app.cuentaBalance.models import *
from app.cuentaResultado.models import *
from app.empresa.models import *
from app.resultado.models import *
from .models import Balance

from django.http import JsonResponse
import datetime

# Create your views here.

def graficos_cuentas(request):
    empresas = Empresa.objects.all()
    return render(request, 'balance/graficos_cuentas.html', {'empresas': empresas})

def obtener_cuentas_por_empresa(request):
    empresa_id = request.GET.get('empresa_id')
    if not empresa_id:
        return JsonResponse({'error': 'ID de empresa no proporcionado'}, status=400)

    try:
        # Filtrar cuentas de balance por la empresa
        cuentas_balance = CuentaBalance.objects.filter(
            idBalance__idEmpresa=empresa_id
        ).values('idCuentaBalance', 'nombre')

        # Filtrar cuentas de resultados por la empresa
        cuentas_resultado = CuentaResultado.objects.filter(
            idResultado__idEmpresa=empresa_id
        ).values('idCuentaResultado', 'nombre')

        # Retornar ambas listas en la respuesta JSON
        return JsonResponse({
            'cuentas_balance': list(cuentas_balance),
            'cuentas_resultado': list(cuentas_resultado),
        })
    except Empresa.DoesNotExist:
        return JsonResponse({'error': 'Empresa no encontrada'}, status=404)

def obtener_datos_cuenta(request):
    cuenta_id = request.GET.get('cuenta_id')
    tipo_cuenta = request.GET.get('tipo_cuenta')
    empresa_id = request.GET.get('empresa_id')

    print(f"cuenta_id: {cuenta_id}, tipo_cuenta: {tipo_cuenta}, empresa_id: {empresa_id}")

    if not cuenta_id or not tipo_cuenta or not empresa_id:
        return JsonResponse({'error': 'Faltan parámetros en la solicitud.'}, status=400)

    datos_por_anio = {}

    try:
        if tipo_cuenta == 'balance':
            # Obtener el código de la cuenta de balance
            c_codigo = CuentaBalance.objects.get(idCuentaBalance=cuenta_id).codigo

            # Filtrar datos relacionados usando el código y la empresa
            datos = CuentaBalance.objects.filter(
                codigo=c_codigo,
                idBalance__idEmpresa=empresa_id
            ).select_related('idBalance')

            for dato in datos:
                anio = dato.idBalance.fecha.year
                datos_por_anio[anio] = datos_por_anio.get(anio, 0) + dato.monto

        elif tipo_cuenta == 'resultado':
            # Obtener el código de la cuenta de resultado
            c_codigo = CuentaResultado.objects.get(idCuentaResultado=cuenta_id).codigo

            # Filtrar datos relacionados usando el código y la empresa
            datos = CuentaResultado.objects.filter(
                codigo=c_codigo,
                idResultado__idEmpresa=empresa_id
            ).select_related('idResultado')

            for dato in datos:
                anio = dato.idResultado.fecha.year
                datos_por_anio[anio] = datos_por_anio.get(anio, 0) + dato.monto

        else:
            return JsonResponse({'error': 'Tipo de cuenta no válido'}, status=400)

        return JsonResponse({'datos': datos_por_anio})

    except CuentaBalance.DoesNotExist:
        return JsonResponse({'error': 'Cuenta de balance no encontrada.'}, status=404)

    except CuentaResultado.DoesNotExist:
        return JsonResponse({'error': 'Cuenta de resultado no encontrada.'}, status=404)

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({'error': 'Ocurrió un error procesando los datos.'}, status=500)



class listaBalance(ListView):
    model = Balance
    template_name = "balance/lista.html"
    context_object_name = "balances"


class crearBalance(CreateView):
    model = Balance
    form_class = BalanceForm
    template_name = "balance/crear.html"
    success_url = reverse_lazy("lista_balance")

    def form_valid(self, form):
        messages.success(self.request, "Balance creado exitosamente.")
        return super().form_valid(form)


class editarBalance(UpdateView):
    model = Balance
    form_class = BalanceForm
    template_name = "balance/editar.html"
    success_url = reverse_lazy("lista_balance")

    def form_valid(self, form):
        messages.success(self.request, "Balance editado exitosamente.")
        return super().form_valid(form)


class eliminarBalance(DeleteView):
    template_name = "balance/eliminar.html"
    model = Balance
    fields = ["nombre", "idEmpresa", "fecha"]
    success_url = reverse_lazy("lista_balance")

    def form_valid(self, form):
        messages.success(self.request, "Balance eliminado exitosamente.")
        return super().form_valid(form)


def calcular_analisis_comparativo(request):
    empresas = Empresa.objects.all()
    balances = Balance.objects.all()
    analisis = []

    if request.method == 'POST':
        empresa1_id = request.POST.get('empresa1')
        empresa2_id = request.POST.get('empresa2')
        balance1_id = request.POST.get('balance1')
        balance2_id = request.POST.get('balance2')

        if not (empresa1_id and empresa2_id and balance1_id and balance2_id):
            messages.error(request, "Por favor, selecciona todas las opciones antes de continuar.")
        else:
            try:
                balance1 = get_object_or_404(Balance, idBalance=balance1_id, idEmpresa_id=empresa1_id)
                balance2 = get_object_or_404(Balance, idBalance=balance2_id, idEmpresa_id=empresa2_id)
            except Balance.DoesNotExist:
                messages.error(request, "No se encontraron balances correspondientes a las empresas seleccionadas.")
                return render(request, 'balance/analisis_comparativo.html', {'empresas': empresas, 'balances': balances, 'analisis': analisis})

            cuentas_balance1 = CuentaBalance.objects.filter(idBalance=balance1)
            cuentas_balance2 = CuentaBalance.objects.filter(idBalance=balance2)

            if not cuentas_balance1 or not cuentas_balance2:
                messages.error(request, "No se encontraron cuentas para los balances seleccionados.")
            else:
                # Obtener los totales específicos
                total_activos_balance1 = next((cuenta.monto for cuenta in cuentas_balance1 if cuenta.codigo == 'tc'), 0)
                total_activos_balance2 = next((cuenta.monto for cuenta in cuentas_balance2 if cuenta.codigo == 'tc'), 0)
                
                total_pasivo_patrimonio_balance1 = next((cuenta.monto for cuenta in cuentas_balance1 if cuenta.codigo == 'Tpmpa'), 0)
                total_pasivo_patrimonio_balance2 = next((cuenta.monto for cuenta in cuentas_balance2 if cuenta.codigo == 'Tpmpa'), 0)

                cuentas_dict = {cuenta.codigo: cuenta for cuenta in cuentas_balance2}

                for cuenta1 in cuentas_balance1:
                    cuenta2 = cuentas_dict.get(cuenta1.codigo)

                    if not cuenta2:
                        continue

                    # Análisis vertical: asignar 100% si es tc, tp, o tpmp
                    if cuenta1.codigo in ['tc', 'tp', 'Tpmpa']:
                        vertical_empresa1 = 100
                        vertical_empresa2 = 100
                    elif cuenta1.codigo.startswith('1'):  # Activos
                        vertical_empresa1 = (cuenta1.monto / total_activos_balance1 * 100) if total_activos_balance1 else 0
                        vertical_empresa2 = (cuenta2.monto / total_activos_balance2 * 100) if total_activos_balance2 else 0
                    elif cuenta1.codigo.startswith('2') or cuenta1.codigo.startswith('3') or cuenta1.codigo.startswith('tpa'):  # Pasivos y Patrimonio
                        vertical_empresa1 = (cuenta1.monto / total_pasivo_patrimonio_balance1 * 100) if total_pasivo_patrimonio_balance1 else 0
                        vertical_empresa2 = (cuenta2.monto / total_pasivo_patrimonio_balance2 * 100) if total_pasivo_patrimonio_balance2 else 0
                    else:
                        vertical_empresa1 = vertical_empresa2 = 0

                    # Análisis horizontal
                    try:
                        horizontal = ((cuenta2.monto - cuenta1.monto) / cuenta1.monto * 100) if cuenta1.monto else 0
                    except ZeroDivisionError:
                        horizontal = 0

                    # Agregar resultado al análisis
                    analisis.append({
                        'cuenta': cuenta1.nombre,
                        'monto_empresa1': cuenta1.monto,
                        'vertical_empresa1': vertical_empresa1,
                        'monto_empresa2': cuenta2.monto,
                        'vertical_empresa2': vertical_empresa2,
                        'horizontal': horizontal
                    })

    return render(request, 'balance/analisis_comparativo.html', {
        'empresas': empresas,
        'balances': balances,
        'analisis': analisis,
    })

def calcular_analisis_individual(request):
    empresas = Empresa.objects.all()
    balances = []
    analisis = []
    empresa_seleccionada = None
    balance1_id = None
    balance2_id = None

    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        balance1_id = request.POST.get('balance1')
        balance2_id = request.POST.get('balance2')

        if not empresa_id:
            messages.error(request, "Por favor, selecciona una empresa.")
        else:
            empresa_seleccionada = int(empresa_id)
            balances = Balance.objects.filter(idEmpresa_id=empresa_id)

            if not (balance1_id and balance2_id):
                messages.error(request, "Por favor, selecciona dos balances.")
            elif balance1_id == balance2_id:
                messages.error(request, "Selecciona dos balances diferentes para la comparación.")
            else:
                # Obtener los balances seleccionados
                balance1 = get_object_or_404(Balance, idBalance=balance1_id, idEmpresa_id=empresa_id)
                balance2 = get_object_or_404(Balance, idBalance=balance2_id, idEmpresa_id=empresa_id)

                # Obtener las cuentas de cada balance
                cuentas_balance1 = CuentaBalance.objects.filter(idBalance=balance1)
                cuentas_balance2 = CuentaBalance.objects.filter(idBalance=balance2)

                if not cuentas_balance1 or not cuentas_balance2:
                    messages.error(request, "No se encontraron cuentas para los balances seleccionados.")
                else:
                    # Obtener los totales específicos para el análisis vertical
                    total_activos1 = next((cuenta.monto for cuenta in cuentas_balance1 if cuenta.codigo == 'tc'), 0)
                    total_pasivo_patrimonio1 = next((cuenta.monto for cuenta in cuentas_balance1 if cuenta.codigo == 'Tpmpa'), 0)

                    total_activos2 = next((cuenta.monto for cuenta in cuentas_balance2 if cuenta.codigo == 'tc'), 0)
                    total_pasivo_patrimonio2 = next((cuenta.monto for cuenta in cuentas_balance2 if cuenta.codigo == 'Tpmpa'), 0)

                    cuentas_dict2 = {cuenta.codigo: cuenta for cuenta in cuentas_balance2}

                    for cuenta1 in cuentas_balance1:
                        cuenta2 = cuentas_dict2.get(cuenta1.codigo)

                        if not cuenta2:
                            continue

                        # Análisis vertical: asignar 100% si es tc o tpmp
                        if cuenta1.codigo == 'tc':
                            vertical_empresa1 = 100
                            vertical_empresa2 = 100
                        elif cuenta1.codigo.startswith('1'):
                            vertical_empresa1 = (cuenta1.monto / total_activos1 * 100) if total_activos1 else 0
                            vertical_empresa2 = (cuenta2.monto / total_activos2 * 100) if total_activos2 else 0
                        elif cuenta1.codigo.startswith('2') or cuenta1.codigo.startswith('3') or cuenta1.codigo.startswith('tpa'):
                            vertical_empresa1 = (cuenta1.monto / total_pasivo_patrimonio1 * 100) if total_pasivo_patrimonio1 else 0
                            vertical_empresa2 = (cuenta2.monto / total_pasivo_patrimonio2 * 100) if total_pasivo_patrimonio2 else 0
                        else:
                            vertical_empresa1 = 100
                            vertical_empresa2 = 100

                        # Análisis horizontal
                        horizontal = ((cuenta2.monto - cuenta1.monto) / cuenta1.monto * 100) if cuenta1.monto else 0

                        # Agregar al análisis
                        analisis.append({
                            'cuenta': cuenta1.nombre,
                            'monto_empresa1': cuenta1.monto,
                            'vertical_empresa1': vertical_empresa1,
                            'monto_empresa2': cuenta2.monto,
                            'vertical_empresa2': vertical_empresa2,
                            'horizontal': horizontal
                        })

    return render(request, 'balance/analisis_individual.html', {
        'empresas': empresas,
        'balances': balances,
        'analisis': analisis,
        'empresa_seleccionada': empresa_seleccionada,
        'balance1_id': balance1_id,
        'balance2_id': balance2_id
    })
