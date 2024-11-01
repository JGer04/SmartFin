from django.urls import path
from app.empresa import views

urlpatterns = [
    path('empresa/', views.listaEmpresa.as_view(), name='lista_empresa'),
    path('empresa/crear/', views.crearEmpresa.as_view(), name='crear_empresa'),
    path('empresa/editar/<int:pk>/', views.editarEmpresa.as_view(), name='editar_empresa'),
    path('empresa/eliminar/<int:pk>/', views.eliminarEmpresa.as_view(), name='eliminar_empresa'),
]
