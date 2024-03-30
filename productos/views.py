from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductosForm
from .models import Productos, Image, Categoria
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin #UPTM es para proteger tu post LRM hace que si un usuario que no haya iniciado sesion, se redireccione a la pagina de registro
from django.contrib.auth.decorators import login_required
from django.db import transaction
# Create your views here.

@login_required

def productos(request):
    prts = Productos.objects.filter(user_id = request.user.id)
    return render(request, "productos.html", {"productos": prts}) 

@login_required
def subir_producto(request):
    if request.method == "POST":
        form = ProductosForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')
        if form.is_valid():
            with transaction.atomic():

                new_producto = form.save(commit=False)
                new_producto.user = request.user
                new_producto.save()

                #Asocia las categorias con el producto

                selected_categorias = request.POST.getlist("categorias")
                new_producto.categorias.set(selected_categorias)
                #Asocia imagenes con el producto
                for f in files:
                    img = Image(image = f)
                    img.save()
                    new_producto.image.add(img)
            messages.success(request,"Se publico su producto")
            return redirect("Productos")
        
    form = ProductosForm()
    return render(request, "productosform.html",{"form":form})

def eliminar_producto(request, producto_id):
    prts = get_object_or_404(Productos, id = producto_id)
    if request.user == prts.user:
        prts.delete()

        return redirect("Productos")
    else:
        messages.error(request, "No puedes eliminar un producto que no es de tu propiedad")
        return redirect("Productos")
    
@login_required 

def det_producto(request, producto_id):
    
    producto = get_object_or_404(Productos, id = producto_id)

    return render(request, "detalles.html",{"producto":producto})    