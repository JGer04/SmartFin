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
from django.core.paginator import Paginator
from io import BytesIO
from django.conf import settings
import tempfile
import shutil
import os

# Create your views here.
def detalleBalance(request,id_balance):
    balance = get_object_or_404(Balance,pk=id_balance)
    cuentas = CuentaBalance.objects.filter(idBalance_id=id_balance)

    paginator = Paginator(cuentas, 10)  # 15 cuentas por página
    page_number = request.GET.get("page")
    cuentas = paginator.get_page(page_number)
    
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

            # Crear un archivo temporal para almacenar el archivo subido
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Escribe el archivo Excel en el archivo temporal
                for chunk in archivo_excel.chunks():
                    temp_file.write(chunk)
                # Almacena la ruta del archivo temporal en la sesión
                request.session['archivo_excel'] = temp_file.name
            
            # Lee el archivo Excel para obtener los nombres de las hojas
            xl = pd.ExcelFile(temp_file.name, engine='openpyxl')
            hojas = xl.sheet_names  # Lista de nombres de las hojas
            
            return redirect('seleccionar_hoja_balance', id_balance=id_balance)

    else:
        form = ExcelUploadForm()

    return render(request, 'cuentaBalance/cargar_excel.html', {
        'form': form,
        'balance': balance
    })


def seleccionar_hoja(request, id_balance):
    balance = get_object_or_404(Balance, pk=id_balance)
    
    # Obtener la ruta del archivo desde la sesión
    archivo_excel_path = request.session.get('archivo_excel')
    
    if archivo_excel_path:
        # Asegúrate de que el archivo existe
        if os.path.exists(archivo_excel_path):
            # Asegúrate de cerrar cualquier referencia al archivo Excel antes de leerlo
            with open(archivo_excel_path, 'rb') as f:
                xl = pd.ExcelFile(f, engine='openpyxl')
                hojas = xl.sheet_names  # Lista de nombres de las hojas
        else:
            # El archivo no existe, puedes redirigir o mostrar un error
            return redirect('cargar_excel', id_balance=id_balance)

    if request.method == "POST":
        hoja_seleccionada = request.POST.get('hoja_seleccionada')
        if hoja_seleccionada:
            with open(archivo_excel_path, 'rb') as f:
                df = pd.read_excel(f, sheet_name=hoja_seleccionada, engine='openpyxl')
            
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

            # Eliminar el archivo temporal después de su uso
            os.remove(archivo_excel_path)

            return redirect('detalle_cuenta_balance', id_balance=id_balance)

    return render(request, 'cuentaBalance/seleccionar_hoja.html', {
        'balance': balance,
        'hojas': hojas
    })
