from django.shortcuts import render, get_object_or_404, redirect
from app.balance.models import Balance
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.balance.forms import BalanceForm
from app.empresa.models import Empresa
from app.cuentaBalance.models import CuentaBalance
from django.core.paginator import Paginator

# Create your views here.


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


def calcular_analisis(request):
    empresas = Empresa.objects.all()
    balances = Balance.objects.all()
    analisis = []

    if request.method == "POST":
        # Obtener los IDs de las empresas y balances seleccionados
        empresa1_id = request.POST.get("empresa1")
        empresa2_id = request.POST.get("empresa2")
        balance1_id = request.POST.get("balance1")
        balance2_id = request.POST.get("balance2")

        print(f"Empresa 1 ID: {empresa1_id}")
        print(f"Empresa 2 ID: {empresa2_id}")
        print(f"Balance 1 ID: {balance1_id}")
        print(f"Balance 2 ID: {balance2_id}")

        # Verificar que todos los campos están seleccionados
        if not (empresa1_id and empresa2_id and balance1_id and balance2_id):
            messages.error(
                request, "Por favor, selecciona todas las opciones antes de continuar."
            )
        else:
            # Obtener los objetos correspondientes de la base de datos
            try:
                balance1 = get_object_or_404(
                    Balance, idBalance=balance1_id, idEmpresa_id=empresa1_id
                )
                balance2 = get_object_or_404(
                    Balance, idBalance=balance2_id, idEmpresa_id=empresa2_id
                )
            except Balance.DoesNotExist:
                messages.error(
                    request,
                    "No se encontraron balances correspondientes a las empresas seleccionadas.",
                )
                return render(
                    request,
                    "balance/analisis1_ver_hor.html",
                    {"empresas": empresas, "balances": balances, "analisis": analisis},
                )

            # Obtener cuentas de cada balance
            cuentas_balance1 = CuentaBalance.objects.filter(idBalance=balance1)
            cuentas_balance2 = CuentaBalance.objects.filter(idBalance=balance2)

            # Verifica si existen cuentas asociadas a los balances seleccionados
            if not cuentas_balance1 or not cuentas_balance2:
                messages.error(
                    request,
                    "No se encontraron cuentas para los balances seleccionados.",
                )
            else:
                # Calcular el total de cada balance para análisis vertical
                total_balance1 = sum(cuenta.monto for cuenta in cuentas_balance1)
                total_balance2 = sum(cuenta.monto for cuenta in cuentas_balance2)

                # Realizar análisis vertical y horizontal
                cuentas_dict = {cuenta.codigo: cuenta for cuenta in cuentas_balance2}

                for cuenta1 in cuentas_balance1:
                    cuenta2 = cuentas_dict.get(cuenta1.codigo)

                    # Si la cuenta de balance 2 no coincide, se omite de la comparación
                    if not cuenta2:
                        continue

                    # Análisis vertical
                    vertical_empresa1 = (
                        (cuenta1.monto / total_balance1 * 100) if total_balance1 else 0
                    )
                    vertical_empresa2 = (
                        (cuenta2.monto / total_balance2 * 100) if total_balance2 else 0
                    )

                    # Análisis horizontal
                    try:
                        horizontal = (
                            ((cuenta2.monto - cuenta1.monto) / cuenta1.monto * 100)
                            if cuenta1.monto
                            else 0
                        )
                    except ZeroDivisionError:
                        horizontal = 0

                    # Agregar resultado al análisis
                    analisis.append(
                        {
                            "cuenta": cuenta1.nombre,
                            "monto_empresa1": cuenta1.monto,
                            "vertical_empresa1": vertical_empresa1,
                            "monto_empresa2": cuenta2.monto,
                            "vertical_empresa2": vertical_empresa2,
                            "horizontal": horizontal,
                        }
                    )

    # # Agregar paginación
    # paginator = Paginator(analisis, 10)  # Muestra 10 elementos por página
    # page_number = request.GET.get("page")
    # page_obj = paginator.get_page(page_number)

    return render(
        request,
        "balance/analisis1_ver_hor.html",
        {
            "empresas": empresas,
            "balances": balances,
            "analisis": analisis,
        },
    )
