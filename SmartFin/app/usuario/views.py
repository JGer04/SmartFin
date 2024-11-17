from django.shortcuts import render, redirect, get_object_or_404
from app.usuario.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy
from django.contrib import messages
from app.usuario.forms import *

def access_users(func):
    def _wrapped_view(self, *args, **kwargs):

        access = AccesoUsuario.objects.get(id_usuario=self.request.user)
        # Ejecuta el método original y obtén el contexto
        context = func(self, *args, **kwargs)
         # Clase propietaria del método
        class_name = self.__class__.__name__

        # Módulo donde está definida la clase
        module_name = self.__class__.__module__

        # Nombre del método decorado
        method_name = func.__name__

        usersito = self.request.user.nom_usuario

        print(f"Accediendo a '{method_name}' de la clase '{class_name}' en el módulo '{module_name}'. CON EL USUARIO LOGEADO: {usersito}. CON ESTE ACCESO: {access.id_opcion.tipo_usuario}. Y ESTE ES EL ID: {access.id_opcion.id_opcion}")
        return context
    return _wrapped_view 

# Create your views here.
def vista404(request):
    return render(request, '404.html')

class listaUsuario(ListView):
    model = Usuario
    template_name = 'usuario/lista.html'
    context_object_name = 'usuarios'

    @access_users
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuarios = self.get_queryset()

        # Mapeo usuario a sus descripciones de opciones
        usuarios_con_opciones = []
        for usuario in usuarios:
            opciones = AccesoUsuario.objects.filter(id_usuario=usuario).select_related('id_opcion')
            opciones_descripciones = [opcion.id_opcion.descripcion for opcion in opciones]
            usuarios_con_opciones.append((usuario, opciones_descripciones))
        
        context['usuarios_con_opciones'] = usuarios_con_opciones
        return context


class crearUsuario(CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/crear.html'
    success_url = reverse_lazy('lista_usuario')

    @access_users
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request,"Usuario creado exitosamente.")
        return super().form_valid(form)

class editarUsuario(UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'usuario/editar.html'
    success_url = reverse_lazy('lista_usuario')

    @access_users
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request,"Usuario editado exitosamente.")
        return super().form_valid(form)
    
class eliminarUsuario(DeleteView):
    template_name = 'usuario/eliminar.html'
    model = Usuario
    fields = ['nom_usuario','password'] 
    success_url = reverse_lazy('lista_usuario')
     
    @access_users
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request,"Usuario eliminado exitosamente.")
        return super().form_valid(form)
    
class detalleUsuario(DetailView):
    model = Usuario
    template_name = 'usuario/detalle.html'
    context_object_name = 'usuario'
    
    @access_users
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.object  # Usuario actual
        opciones = AccesoUsuario.objects.filter(id_usuario=usuario).select_related('id_opcion')
        context['opciones'] = [opcion.id_opcion.descripcion for opcion in opciones]
        return context


#Views Opcion
class listaOpcion(ListView):
    model = OpcionForm
    template_name = 'opcion/lista.html'
    context_object_name = 'opciones'

class crearOpcion(CreateView):
    model = OpcionForm
    form_class = OpcionFormForm
    template_name = 'opcion/crear.html'
    success_url = reverse_lazy('lista_opcion')
    
    def form_valid(self, form):
        messages.success(self.request,"opcion creada exitosamente.")
        return super().form_valid(form)

class editarOpcion(UpdateView):
    model = OpcionForm
    form_class = OpcionFormForm
    template_name = 'opcion/editar.html'
    success_url = reverse_lazy('lista_opcion')
    
    def form_valid(self, form):
        messages.success(self.request,"opcion editada exitosamente.")
        return super().form_valid(form)
    
class eliminarOpcion(DeleteView):
    template_name = 'opcion/eliminar.html'
    model = OpcionForm
    fields = ['nom_opcion','password'] 
    success_url = reverse_lazy('lista_opcion')

    def form_valid(self, form):
        messages.success(self.request,"opcion eliminada exitosamente.")
        return super().form_valid(form)
    
class detalleOpcion(DetailView):
    model = OpcionForm
    template_name = 'opcion/detalle.html'
    context_object_name = 'opcion'

class AsignarAccesoForm(forms.Form):
    usuario = forms.ModelChoiceField(queryset=Usuario.objects.all(), label="Usuario")
    opciones = forms.ModelMultipleChoiceField(
        queryset=OpcionForm.objects.all(),
        label="Opciones",
        widget=forms.CheckboxSelectMultiple,
        required=True
    )

class AsignarAccesoView(View):
    template_name = 'opcion/asignar_acceso.html'

    def get(self, request, *args, **kwargs):
        form = AsignarAccesoForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = AsignarAccesoForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            opciones = form.cleaned_data['opciones']

            # Eliminar accesos existentes del usuario
            AccesoUsuario.objects.filter(id_usuario=usuario).delete()

            # Crear los nuevos accesos
            for opcion in opciones:
                AccesoUsuario.objects.create(
                    id_usuario=usuario,
                    id_opcion=opcion
                )

            # Redirigir o mostrar mensaje de éxito
            return redirect('asignar_acceso')  # Cambia 'asignar_acceso' por el nombre de tu URL de éxito
        return render(request, self.template_name, {'form': form})


