from django.shortcuts import render
from app.resultado.models import Resultado
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

