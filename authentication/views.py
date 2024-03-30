from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import View
from django.contrib import messages

class VRegisto(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "registro.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Se ha registrado correctamente")
            return redirect("Home")

        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

            return render(request, "registro.html", {"form":form})    
def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username = username, password = password) #Si los datos son iguales, devuelve un usuario

            if user is not None:
                login(request, user)

                return redirect("Home")
            
            else:
                messages.error(request, "No se ha podido iniciar sesion, contraseña y/o correo incorrectos")           
        else:
            messages.error(request,"informacion incorrecta")

            

    form = AuthenticationForm()
    return render(request, "login.html", {"form":form})

def Logout(request):
    logout(request)

    return redirect("Home")

# Create your views here.
