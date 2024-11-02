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
            
            # Lee el archivo Excel
            df = pd.read_excel(archivo_excel, engine='openpyxl')
            
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
            
            return redirect('detalle_cuenta_resultado', id_resultado=id_resultado)

    else:
        form = ExcelUploadForm()

    return render(request, 'cuentaResultado/cargar_excel.html', {'form': form, 'resultado': resultado})
