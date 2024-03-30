from django.urls import path
from . import views

urlpatterns = [
    path("",views.productos, name="Productos"),
    path("upload/",views.subir_producto, name="Upload"),
    path("delete/<int:producto_id>",views.eliminar_producto, name="Delete"),
    path("<int:producto_id>", views.det_producto, name="Detalles")
]