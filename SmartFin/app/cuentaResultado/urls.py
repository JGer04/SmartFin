from django.urls import path
from app.cuentaResultado import views

urlpatterns = [
    path('resultado/<int:id_resultado>/detalle/',views.detalleResultado, name='detalle_cuenta_resultado'),
    path('resultado/<int:id_resultado>/crear-cuenta/',views.crearCuenta.as_view(), name='crear_cuenta_resultado'),
    path('resultado/<int:id_resultado>/subir-excel/',views.cargar_cuentas_excel, name='crear_cuenta_excel_resultado'),
    path('resultado/subir-hoja/<int:id_resultado>/', views.seleccionar_hoja, name='seleccionar_hoja_resultado'),
]
