from django.shortcuts import render
from productos.models import Productos, Categoria


# Create your views here.
def home(request):

    productos = Productos.objects.all()
    categorias = Categoria.objects.all()
    
    return render(request,"home.html", {"productos":productos, "categorias":categorias})

def buscar(request, categoria_id = None):


    #Inicializamos una variable de tipo queryset

    f_productos = ""

    #Traemos la busqueda

    busqueda = request.GET.get("buscar","")

    #Activamos el sistema de filtro sobre todos los productos
    
    #Utilizamos get_category_from_search para ver si la busqueda de por si es una categoria
    #Esta funcion me da un boolean y un objeto 4
    #Esta funcion la cree para que cuando un usuario busque autos, les traiga todos los autos disponibles gracias a las categorias
    #Si no tuviera esta funcion, no les traeria nada ya que ningun producto tiene como titulo autos

    es_categoria, categoria =Categoria.objects.get_category_from_search(busqueda)
    if es_categoria == True:
        f_productos = Productos.objects.get_by_filter(categoria.id)
    else:
        f_productos = Productos.objects.get_by_filter(categoria_id)

    found = Productos.objects.get_by_letters(f_productos,busqueda)
    # Luego de traer los productos encontrados, tambien traemos un conjunto de categorias encontrada perteneciente a los productos
 
    categorias = Categoria.objects.get_by_product(found)

    
    return render(request,"found.html", {"found": found, "categorias": categorias})

def nosotros(request):

    return render(request, "nosotros.html")