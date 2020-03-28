from django import forms
from .models import Product


class Productform(forms.ModelForm):
    class Meta:
        model = Product
        widgets={
        'descript':forms.Textarea(attrs={'class':'text-input','placeholder':'Product description'}),
        'brand':forms.TextInput(attrs={'class':'text-input','placeholder':'Brand example: Nike, Addidas,Samsung'}),
        'size':forms.TextInput(attrs={'class':'text-input','placeholder':'Available sizes, example: 12 inches, 32square ft,41'}),
        'color':forms.TextInput(attrs={'class':'text-input','placeholder':'Available colors, example: red, yellow,blue'}),
        'state':forms.Select(attrs={'class':'text-select'}),
        'category':forms.Select(attrs={'class':'text-select'}),
        'subcategory':forms.Select(attrs={'class':'text-select'}),
        'productname':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product name'}),
        'model':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product model'}),
        'location':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product location'}),
        'pdprice':forms.TextInput(attrs={'class':'text-input','placeholder':'Example "2000" digits only '}),
        }
        exclude=('salesprice','sales','created','slug','user','status')
        fields =('pdprice','state','location','brand','category','subcategory','productname','picone','pictwo','picthree','picfour','descript','model','size','color')