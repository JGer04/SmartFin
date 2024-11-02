from django.urls import path
from app.cuentaBalance import views

urlpatterns = [
    path('balance/<int:id_balance>/detalle/',views.detalleBalance, name='detalle_cuenta_balance'),
    path('balance/<int:id_balance>/crear-cuenta/',views.crearCuenta.as_view(), name='crear_cuenta_balance'),
    path('balance/<int:id_balance>/subir-excel/',views.cargar_cuentas_excel, name='crear_cuenta_excel_balance'),
]
