from django.urls import path
from app.cuentaResultado import views

urlpatterns = [
    path('resultado/<int:id_resultado>/detalle/',views.detalleResultado, name='detalle_cuenta_resultado'),
    path('resultado/<int:id_resultado>/crear-cuenta/',views.crearCuenta.as_view(), name='crear_cuenta_resultado'),
]
