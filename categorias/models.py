from django.db import models


# Create your models here.

class CategoriaManager(models.Manager):
    def get_category_from_search(self, busqueda):
        for categoria in self.all():
            if categoria.nombre.lower() in busqueda.lower():
                return True, categoria #Retorna una tupla enviandole el objeto categoria encontrado
             
        return False, None     #Retorna el false y un vacio
    def get_by_product(self, productos):
        """
        extraidos = []
        for producto in productos:
            for categoria in producto.categorias.all():
                if categoria.nombre not in extraidos:
                    extraidos.append(categoria) Esto tambien se puede hacer de la siguiente manera
        return extraidos                          
                    """
        
        
        return list(set(categoria for producto in productos for categoria in producto.categorias.all()))
#             Lista Conj var almacenadora| bucle|            |bucle      
        


class Categoria(models.Model):
    nombre = models.CharField(max_length=40)
    is_selected = models.BooleanField(default = False) #Me servira para diseño
    objects = CategoriaManager()

    def __str__(self):
        return self.nombre
    