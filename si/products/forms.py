from django import forms


class FormularioProducts(forms.Form):


    """Modelo de formulario para productos en general"""
    name = forms.CharField(max_length=30)
    category = forms.CharField(max_length=30)
    description = forms.CharField(max_length=100)
    price = forms.FloatField()
    stock = forms.IntegerField()
    image = forms.ImageField(required=False)