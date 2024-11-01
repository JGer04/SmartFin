from django.shortcuts import render
from app.empresa.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from app.empresa.forms import empresaForm

# Create your views here.
class listaEmpresa(ListView):
    model = Empresa
    template_name = 'empresa/lista.html'
    context_object_name = 'empresas'

class crearEmpresa(CreateView):
    model = Empresa
    form_class = empresaForm
    template_name = 'empresa/crear.html'
    success_url = reverse_lazy('lista_empresa')
    
    def form_valid(self, form):
        messages.success(self.request,"Empresa creada exitosamente.")
        return super().form_valid(form)

class editarEmpresa(UpdateView):
    model = Empresa
    form_class = empresaForm
    template_name = 'empresa/editar.html'
    success_url = reverse_lazy('lista_empresa')
    
    def form_valid(self, form):
        messages.success(self.request,"Empresa editada exitosamente.")
        return super().form_valid(form)
    
class eliminarEmpresa(DeleteView):
    template_name = 'empresa/eliminar.html'
    model = Empresa
    fields = ['nombre','direccion','telefono','sector']
    success_url = reverse_lazy('lista_empresa')

    def form_valid(self, form):
        messages.success(self.request,"Empresa eliminada exitosamente.")
        return super().form_valid(form)

