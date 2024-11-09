from django.urls import path
from app.resultado import views

urlpatterns = [
    path('resultado/',views.listaResultado.as_view(), name='lista_resultado'),
    path('resultado/crear/',views.crearResultado.as_view(), name='crear_resultado'),
    path('resultado/editar/<int:pk>/',views.editarResultado.as_view(), name='editar_resultado'),
    path('resultado/<int:pk>/',views.eliminarResultado.as_view(), name='eliminar_resultado'),
    path('resultado/analisis-comparativo', views.calcular_analisis_comparativo, name='calcular_analisis_resultado_comparativo'),
    path('resultado/analisis-individual', views.calcular_analisis_individual, name='calcular_analisis_resultado_individual'),
]
