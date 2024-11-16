from django.urls import path
from app.usuario.views import *

urlpatterns = [
    path('usuario/', listaUsuario.as_view(), name='lista_usuario'),
    path('usuario/crear/', crearUsuario.as_view(), name='crear_usuario'),
    path('usuario/editar/<int:pk>/', editarUsuario.as_view(), name='editar_usuario'),
    path('usuario/eliminar/<int:pk>/', eliminarUsuario.as_view(), name='eliminar_usuario'),
    path('usuario/detalle/<int:pk>/', detalleUsuario.as_view(), name='detalle_usuario'),  # Nueva ruta
]
