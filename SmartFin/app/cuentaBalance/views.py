from django.shortcuts import render, get_object_or_404, redirect
from app.cuentaBalance.models import CuentaBalance
from app.balance.models import Balance
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.cuentaBalance.forms import CuentaBalanceForm

# Create your views here.
def detalleBalance(request,id_balance):
    balance = get_object_or_404(Balance,pk=id_balance)
    cuentas = CuentaBalance.objects.filter(idBalance_id=id_balance)
    context = {
        'balance':balance,
        'cuentas':cuentas
    }
    return render(request, 'cuentaBalance/detalle.html',context)

class crearCuenta(CreateView):
    model = CuentaBalance
    template_name = 'cuentaBalance/crear.html'
    form_class = CuentaBalanceForm
    success_url = reverse_lazy('cuenta_balance_detalle')

    def form_valid(self, form):
        # Obtener el balance actual usando el id en la URL
        id_balance = self.kwargs['id_balance']
        balance = get_object_or_404(Balance, pk=id_balance)
        messages.success(self.request, "Cuenta creada exitosamente.")
        form.instance.idBalance = balance  # Asignar el balance a la cuenta
        return super().form_valid(form)

    def get_success_url(self):
        # Redirigir de vuelta a la página de detalles del balance
        return reverse_lazy('detalle_cuenta_balance', kwargs={'id_balance': self.kwargs['id_balance']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el balance actual usando el id en la URL
        id_balance = self.kwargs['id_balance']
        balance = get_object_or_404(Balance, pk=id_balance)
        context['balance'] = balance  # Pasar el balance al contexto
        return context
    