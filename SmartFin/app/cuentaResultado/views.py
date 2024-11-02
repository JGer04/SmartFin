from django.shortcuts import render, get_object_or_404, redirect
from app.cuentaResultado.models import CuentaResultado
from app.resultado.models import Resultado
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.cuentaResultado.forms import CuentaResultadoForm

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
