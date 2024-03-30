from django.urls import path
from . import views

app_name = "authentication"

urlpatterns = [
    path("registrar/",views.VRegisto.as_view(), name="Registrarse"),
    path("login/",views.Login, name="Login"),
    path("logout/",views.Logout,name="Logout")
]