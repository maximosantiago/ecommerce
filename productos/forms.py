from django import forms
from .models import Productos
from .models import Categoria

class ProductosForm(forms.ModelForm):
    titulo = forms.CharField(widget=forms.TextInput(attrs={
        "class":"titulo-producto"
    }))
    contenido = forms.CharField(widget=forms.Textarea(attrs={
        "class":"contenido-producto"
    }))
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={
        "class": "imagen-producto",
        "Multiple":"True"}),
        required=False)

    class Meta:
        model = Productos
        fields = ("titulo", "contenido", "image", "precio", "categorias")

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.fields["categorias"].queryset = Categoria.objects.exclude(nombre = "Todos")

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ("nombre",)