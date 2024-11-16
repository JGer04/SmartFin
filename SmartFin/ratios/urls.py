# ratios/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_cruds, name='menu_cruds'),
    path('secciones/', views.lista_secciones, name='lista_secciones'),
    path('secciones/crear/', views.crear_seccion, name='crear_seccion'),
    path('secciones/<int:pk>/editar/', views.editar_seccion, name='editar_seccion'),
    path('secciones/<int:pk>/eliminar/', views.eliminar_seccion, name='eliminar_seccion'),

    path('subsecciones/', views.lista_subsecciones, name='lista_subsecciones'),
    path('subsecciones/crear/', views.crear_subseccion, name='crear_subseccion'),
    path('subsecciones/<int:pk>/editar/', views.editar_subseccion, name='editar_subseccion'),
    path('subsecciones/<int:pk>/eliminar/', views.eliminar_subseccion, name='eliminar_subseccion'),

    path('razones/', views.lista_razones, name='lista_razones'),
    path('razones/crear/', views.crear_razon, name='crear_razon'),
    path('razones/<int:pk>/editar/', views.editar_razon, name='editar_razon'),
    path('razones/<int:pk>/eliminar/', views.eliminar_razon, name='eliminar_razon'),
    path('calcular_ratio/<int:id_balance>/', views.calcular_ratios, name='calcular_ratio'),
]
