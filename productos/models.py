from django.db import models
from django.contrib.auth.models import User
from categorias.models import Categoria
# Create your models here.

class ProductosManager(models.Manager):

    def get_by_filter(self, categoria_id):
        #esta funcion debera devolver todos los productos segun la categoria
        
        id = categoria_id #Creo una varible id cuyo valor sea el de pasado por parametros


        #Traigo la categoria

        if id == None:
            for categoria in Categoria.objects.all(): #Si id es none, es decir, no se paso ningun id por el request
                if categoria.is_selected == True:       #Tendra que tomar el id del ultimo objeto activado
                    id = categoria.id


        categoria_found = Categoria.objects.get(id = id)


        #A su vez, debo desactivar las categorias que estan seleccionadas en el caso que haya habido un cambio de categorias

        for categoria in Categoria.objects.all():
            if categoria.is_selected == True and categoria.id != categoria_found.id:
                categoria.is_selected = False
                categoria.save()

        #guardo los cambios para la nueva categoria

        
        categoria_found.is_selected = True
        categoria_found.save()

        if categoria_found.nombre== "Todos":     
            return self.all()
       
        return self.filter(categorias = categoria_found)
    
    def get_by_letters(self,productos, busqueda):

       
        found = []
        for producto in productos:
            if busqueda.capitalize() in producto.titulo.capitalize():
                found.append(producto)

        if len(found) == 0:
            return productos
        return found        



class Productos(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    titulo = models.CharField(max_length = 70)
    contenido = models.TextField()
    categorias = models.ManyToManyField(Categoria, blank=True)
    image = models.ManyToManyField("Image", blank=True)
    precio = models.DecimalField(max_digits = 20, decimal_places = 2)

    objects = ProductosManager()


class Image(models.Model):
    image = models.ImageField(upload_to="imagenes_productos/")


