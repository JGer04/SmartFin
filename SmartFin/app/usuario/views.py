from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from app.usuario.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from app.usuario.forms import UsuarioForm

# Create your views here.
class listaUsuario(ListView):
    model = Usuario
    template_name = 'usuario/lista.html'
    context_object_name = 'usuarios'

class crearUsuario(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('lista_usuario')
    
    def form_valid(self, form):
        messages.success(self.request,"Usuario creada exitosamente.")
        return super().form_valid(form)

class editarUsuario(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/editar.html'
    success_url = reverse_lazy('lista_usuario')
    
    def form_valid(self, form):
        messages.success(self.request,"Usuario editada exitosamente.")
        return super().form_valid(form)
    
class eliminarUsuario(DeleteView):
    template_name = 'usuario/eliminar.html'
    model = Usuario
    fields = ['nom_usuario','password'] 
    success_url = reverse_lazy('lista_usuario')

    def form_valid(self, form):
        messages.success(self.request,"Usuario eliminada exitosamente.")
        return super().form_valid(form)
    
class detalleUsuario(DetailView):
    model = Usuario
    template_name = 'usuario/detalle.html'
    context_object_name = 'usuario'

