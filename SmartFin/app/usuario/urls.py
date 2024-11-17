from django.urls import path
from app.usuario.views import *

urlpatterns = [
    path('usuario/', listaUsuario.as_view(), name='lista_usuario'),
    path('usuario/crear/', crearUsuario.as_view(), name='crear_usuario'),
    path('usuario/editar/<int:pk>/', editarUsuario.as_view(), name='editar_usuario'),
    path('usuario/eliminar/<int:pk>/', eliminarUsuario.as_view(), name='eliminar_usuario'),
    path('usuario/detalle/<int:pk>/', detalleUsuario.as_view(), name='detalle_usuario'),

    #URLs para opciones
    path('opcion/', listaOpcion.as_view(), name='lista_opcion'),
    path('opcion/crear/', crearOpcion.as_view(), name='crear_opcion'),
    path('opcion/editar/<int:pk>/', editarOpcion.as_view(), name='editar_opcion'),
    path('opcion/eliminar/<int:pk>/', eliminarOpcion.as_view(), name='eliminar_opcion'),
    path('opcion/detalle/<int:pk>/', detalleOpcion.as_view(), name='detalle_opcion'),

    path('opcion/asignar-acceso/', AsignarAccesoView.as_view(), name='asignar_acceso'),

    path('404/', vista404, name='404'),
]
