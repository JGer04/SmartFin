from django.shortcuts import render, get_object_or_404, redirect
from app.cuentaResultado.models import CuentaResultado
from app.resultado.models import Resultado
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.cuentaResultado.forms import CuentaResultadoForm
import pandas as pd
from django.http import HttpResponse
from .forms import ExcelUploadForm
import os
import tempfile

# Create your views here.
def detalleResultado(request,id_resultado):
    resultado = get_object_or_404(Resultado,pk=id_resultado)
    cuentas = CuentaResultado.objects.filter(idResultado_id=id_resultado)
    context = {
        'resultado':resultado,
        'cuentas':cuentas
    }
    return render(request, 'cuentaResultado/detalle.html',context)

class crearCuenta(CreateView):
    model = CuentaResultado
    template_name = 'cuentaResultado/crear.html'
    form_class = CuentaResultadoForm
    success_url = reverse_lazy('cuenta_resultado_detalle')

    def form_valid(self, form):
        id_resultado = self.kwargs['id_resultado']
        resultado = get_object_or_404(Resultado, pk=id_resultado)
        messages.success(self.request, "Cuenta creada exitosamente.")
        form.instance.idResultado = resultado
        return super().form_valid(form)

    def get_success_url(self):

        return reverse_lazy('detalle_cuenta_resultado', kwargs={'id_resultado': self.kwargs['id_resultado']})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_resultado = self.kwargs['id_resultado']
        resultado = get_object_or_404(Resultado, pk=id_resultado)
        context['resultado'] = resultado
        return context
    
def cargar_cuentas_excel(request, id_resultado):
    resultado = get_object_or_404(Resultado, pk=id_resultado)

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
            
            return redirect('seleccionar_hoja_resultado', id_resultado=id_resultado)

    else:
        form = ExcelUploadForm()

    return render(request, 'cuentaResultado/cargar_excel.html', {
        'form': form,
        'resultado': resultado
    })


def seleccionar_hoja(request, id_resultado):
    resultado = get_object_or_404(Resultado, pk=id_resultado)
    
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
            return redirect('cargar_excel', id_balance=id_resultado)

    if request.method == "POST":
        hoja_seleccionada = request.POST.get('hoja_seleccionada')
        if hoja_seleccionada:
            with open(archivo_excel_path, 'rb') as f:
                df = pd.read_excel(f, sheet_name=hoja_seleccionada, engine='openpyxl')
            
            # Filtrar filas válidas donde el código es numérico
            for _, row in df.iterrows():
                if pd.notnull(row['codigo']) and pd.notnull(row['nombre']):
                    # Crea la cuenta balance
                    CuentaResultado.objects.create(
                        idResultado=resultado,
                        codigo=row['codigo'],
                        nombre=row['nombre'][:50],  # Trunca a 50 caracteres si es necesario
                        monto=row['monto'] if pd.notnull(row['monto']) else 0.0  # Maneja montos nulos
                    )

            # Eliminar el archivo temporal después de su uso
            os.remove(archivo_excel_path)

            return redirect('detalle_cuenta_resultado', id_resultado=id_resultado)

    return render(request, 'cuentaResultado/seleccionar_hoja.html', {
        'resultado': resultado,
        'hojas': hojas
    })
