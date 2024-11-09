from django.shortcuts import render, get_object_or_404, redirect
from app.resultado.models import Resultado
from app.empresa.models import Empresa
from app.cuentaResultado.models import CuentaResultado
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.resultado.forms import ResultadoForm
# Create your views here.

class listaResultado(ListView):
    model = Resultado
    template_name = 'resultado/lista.html'
    context_object_name = 'resultados'

class crearResultado(CreateView):
    model = Resultado
    form_class = ResultadoForm
    template_name = 'resultado/crear.html'
    success_url = reverse_lazy('lista_resultado')

    def form_valid(self, form):
        messages.success(self.request, "E. Resultado creado exitosamente.")
        return super().form_valid(form)
    
class editarResultado(UpdateView):
    model = Resultado
    form_class = ResultadoForm
    template_name = 'resultado/editar.html'
    success_url = reverse_lazy('lista_resultado')

    def form_valid(self, form):
        messages.success(self.request, "E. Resultado editado exitosamente.")
        return super().form_valid(form)
    
class eliminarResultado(DeleteView):
    template_name = 'resultado/eliminar.html'
    model = Resultado
    fields = ['nombre','idEmpresa','fecha']
    success_url = reverse_lazy('lista_resultado')

    def form_valid(self, form):
        messages.success(self.request,"E. Resultado eliminado exitosamente.")
        return super().form_valid(form)


def calcular_analisis_comparativo(request):
    empresas = Empresa.objects.all()
    resultados = Resultado.objects.all()
    analisis = []

    if request.method == 'POST':
        empresa1_id = request.POST.get('empresa1')
        empresa2_id = request.POST.get('empresa2')
        resultado1_id = request.POST.get('resultado1')
        resultado2_id = request.POST.get('resultado2')

        if not (empresa1_id and empresa2_id and resultado1_id and resultado2_id):
            messages.error(request, "Por favor, selecciona todas las opciones antes de continuar.")
        else:
            try:
                resultado1 = get_object_or_404(Resultado, idResultado=resultado1_id, idEmpresa_id=empresa1_id)
                resultado2 = get_object_or_404(Resultado, idResultado=resultado2_id, idEmpresa_id=empresa2_id)
            except Resultado.DoesNotExist:
                messages.error(request, "No se encontraron E. Resultados correspondientes a las empresas seleccionadas.")
                return render(request, 'resultado/analisis_comparativo.html', {'empresas': empresas, 'resultados': resultados, 'analisis': analisis})

            cuentas_resultado1 = CuentaResultado.objects.filter(idResultado=resultado1)
            cuentas_resultado2 = CuentaResultado.objects.filter(idResultado=resultado2)

            if not cuentas_resultado1 or not cuentas_resultado2:
                messages.error(request, "No se encontraron cuentas para los E. Resultados seleccionados.")
            else:
                # Obtener los totales específicos
                total_ventas_resultado1 = next((cuenta.monto for cuenta in cuentas_resultado1 if cuenta.codigo == '41'), 0)
                total_ventas_resultado2 = next((cuenta.monto for cuenta in cuentas_resultado2 if cuenta.codigo == '41'), 0)
                
                #total_pasivo_patrimonio_resultado1 = next((cuenta.monto for cuenta in cuentas_resultado1 if cuenta.codigo == 'Tpmpa'), 0)
                #total_pasivo_patrimonio_resultado2 = next((cuenta.monto for cuenta in cuentas_resultado2 if cuenta.codigo == 'Tpmpa'), 0)

                cuentas_dict = {cuenta.codigo: cuenta for cuenta in cuentas_resultado2}

                for cuenta1 in cuentas_resultado1:
                    cuenta2 = cuentas_dict.get(cuenta1.codigo)

                    if not cuenta2:
                        continue

                    # Análisis vertical: usar las que no tiene código numérico
                    if cuenta1.codigo in ['41']:
                        vertical_empresa1 = 100
                        vertical_empresa2 = 100
                    elif cuenta1.codigo.startswith('4') or cuenta1.codigo.startswith('5')  or cuenta1.codigo.startswith('ub') or cuenta1.codigo.startswith('uo') or cuenta1.codigo.startswith('ua') or cuenta1.codigo.startswith('un'):  # Activos
                        vertical_empresa1 = (cuenta1.monto / total_ventas_resultado1 * 100) if total_ventas_resultado1 else 0
                        vertical_empresa2 = (cuenta2.monto / total_ventas_resultado2 * 100) if total_ventas_resultado2 else 0
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

    return render(request, 'resultado/analisis_comparativo.html', {
        'empresas': empresas,
        'resultados': resultados,
        'analisis': analisis,
    })

def calcular_analisis_individual(request):
    empresas = Empresa.objects.all()
    resultados = []
    analisis = []
    empresa_seleccionada = None
    resultado1_id = None
    resultado2_id = None

    if request.method == 'POST':
        empresa_id = request.POST.get('empresa')
        resultado1_id = request.POST.get('resultado1')
        resultado2_id = request.POST.get('resultado2')

        if not empresa_id:
            messages.error(request, "Por favor, selecciona una empresa.")
        else:
            empresa_seleccionada = int(empresa_id)
            resultados = Resultado.objects.filter(idEmpresa_id=empresa_id)

            if not (resultado1_id and resultado2_id):
                messages.error(request, "Por favor, selecciona dos E. Resultados.")
            elif resultado1_id == resultado2_id:
                messages.error(request, "Selecciona dos E. Resultados diferentes para la comparación.")
            else:
                # Obtener los ER seleccionados
                resultado1 = get_object_or_404(Resultado, idResultado=resultado1_id, idEmpresa_id=empresa_id)
                resultado2 = get_object_or_404(Resultado, idResultado=resultado2_id, idEmpresa_id=empresa_id)

                # Obtener las cuentas de cada ER
                cuentas_resultado1 = CuentaResultado.objects.filter(idResultado=resultado1)
                cuentas_resultado2 = CuentaResultado.objects.filter(idResultado=resultado2)

                if not cuentas_resultado1 or not cuentas_resultado2:
                    messages.error(request, "No se encontraron cuentas para los E. Resultados seleccionados.")
                else:
                    # Obtener los totales específicos para el análisis vertical
                    total_ventas1 = next((cuenta.monto for cuenta in cuentas_resultado1 if cuenta.codigo == '41'), 0)
                    #total_pasivo_patrimonio1 = next((cuenta.monto for cuenta in cuentas_resultado1 if cuenta.codigo == 'Tpmpa'), 0)

                    total_ventas2 = next((cuenta.monto for cuenta in cuentas_resultado2 if cuenta.codigo == '41'), 0)
                    #total_pasivo_patrimonio2 = next((cuenta.monto for cuenta in cuentas_resultado2 if cuenta.codigo == 'Tpmpa'), 0)

                    cuentas_dict2 = {cuenta.codigo: cuenta for cuenta in cuentas_resultado2}

                    for cuenta1 in cuentas_resultado1:
                        cuenta2 = cuentas_dict2.get(cuenta1.codigo)

                        if not cuenta2:
                            continue

                        # Análisis vertical: usar el asignar 100% si es código numerico
                        if cuenta1.codigo == '41':
                            vertical_empresa1 = 100
                            vertical_empresa2 = 100
                        elif cuenta1.codigo.startswith('4') or cuenta1.codigo.startswith('5') or cuenta1.codigo.startswith('ub') or cuenta1.codigo.startswith('uo') or cuenta1.codigo.startswith('ua') or cuenta1.codigo.startswith('un'):
                            vertical_empresa1 = (cuenta1.monto / total_ventas1 * 100) if total_ventas1 else 0
                            vertical_empresa2 = (cuenta2.monto / total_ventas2 * 100) if total_ventas2 else 0
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

    return render(request, 'resultado/analisis_individual.html', {
        'empresas': empresas,
        'resultados': resultados,
        'analisis': analisis,
        'empresa_seleccionada': empresa_seleccionada,
        'resultado1_id': resultado1_id,
        'resultado2_id': resultado2_id
    })