from django.urls import path
from app.balance import views

urlpatterns = [
    path('balance/',views.listaBalance.as_view(), name='lista_balance'),
    path('balance/crear/',views.crearBalance.as_view(), name='crear_balance'),
    path('balance/editar/<int:pk>/',views.editarBalance.as_view(), name='editar_balance'),
    path('balance/<int:pk>/',views.eliminarBalance.as_view(), name='eliminar_balance'),

    #path('balance/comparar/', views.compararEmpresa, name='comparar_analisis_balance'),
    path('balance/analisis-comparativo', views.calcular_analisis_comparativo, name='calcular_analisis_balance_comparativo'),
    path('balance/analisis-individual', views.calcular_analisis_individual, name='calcular_analisis_balance_individual'),
]
