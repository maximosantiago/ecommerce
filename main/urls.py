from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name = "Home"),
    path("buscar/",views.buscar, name="Search"),
    path("buscar/<int:categoria_id>", views.buscar, name="Filter"),
    path("nosotros/", views.nosotros, name = "Nosotros")

]