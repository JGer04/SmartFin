from django.shortcuts import render, get_object_or_404, redirect
from app.cuentaBalance.models import CuentaBalance
from app.balance.models import Balance
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.cuentaBalance.forms import CuentaBalanceForm
import pandas as pd
from django.http import HttpResponse
from .forms import ExcelUploadForm

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
    
def cargar_cuentas_excel(request, id_balance):
    balance = get_object_or_404(Balance, pk=id_balance)

    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            archivo_excel = request.FILES['archivo_excel']
            
            # Lee el archivo Excel
            df = pd.read_excel(archivo_excel, engine='openpyxl')
            
            # Filtrar filas válidas donde el código es numérico
            for _, row in df.iterrows():
                if pd.notnull(row['codigo']) and pd.notnull(row['nombre']):
                    # Crea la cuenta balance
                    CuentaBalance.objects.create(
                        idBalance=balance,
                        codigo=row['codigo'],
                        nombre=row['nombre'][:50],  # Trunca a 50 caracteres si es necesario
                        monto=row['monto'] if pd.notnull(row['monto']) else 0.0  # Maneja montos nulos
                    )
            
            return redirect('detalle_cuenta_balance', id_balance=id_balance)

    else:
        form = ExcelUploadForm()

    return render(request, 'cuentaBalance/cargar_excel.html', {'form': form, 'balance': balance})
    