from django.urls import path
from . import views

urlpatterns = [
    path("mp/<int:producto_id>", views.pagos, name="Pagos"),
    path("mp/exitoso",views.exito, name="Exitoso"),
    path("mp/notificacion", views.mercadopago_notification, name= "Notificaciones")
]