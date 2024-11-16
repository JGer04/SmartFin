from django.urls import path
from app.empresa.views import *

urlpatterns = [
    path('empresa/', listaEmpresa.as_view(), name='lista_empresa'),
    path('empresa/crear/', crearEmpresa.as_view(), name='crear_empresa'),
    path('empresa/editar/<int:pk>/', editarEmpresa.as_view(), name='editar_empresa'),
    path('empresa/eliminar/<int:pk>/', eliminarEmpresa.as_view(), name='eliminar_empresa'),
    path('empresa/detalle/<int:pk>/', detalleEmpresa.as_view(), name='detalle_empresa'),  # Nueva ruta
]
