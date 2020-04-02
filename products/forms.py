from django import forms
from .models import Product


class Productform(forms.ModelForm):
    class Meta:
        model = Product
        widgets={
        'descript':forms.Textarea(attrs={'class':'text-input','placeholder':'Product description'}),
        'brand':forms.TextInput(attrs={'class':'text-input','placeholder':'Brand example: Nike, Addidas,Samsung'}),
        'size':forms.TextInput(attrs={'class':'text-input','placeholder':'Product size, example: 12 inches, 32square ft,41'}),
        'state':forms.Select(attrs={'class':'text-select'}),
        'category':forms.Select(attrs={'class':'text-select'}),
        'subcategory':forms.Select(attrs={'class':'text-select'}),
        'productname':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product name'}),
        'model':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product model'}),
        'location':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product location'}),
        'pdprice':forms.TextInput(attrs={'class':'text-input','placeholder':'Example "2000" digits only '}),
        }
        exclude=('salesprice','sales','created','slug','user','status')
        fields =('pdprice','state','location','brand','category','subcategory','productname','picone','pictwo','picthree','picfour','descript','model','size')

# add product sizes

class Productcolors(forms.ModelForm):
    class Meta:
        model = Product
        widgets={
        'color':forms.TextInput(attrs={'class':'text-input','placeholder':'example red'}),

        }
        exclude=('pdprice','state','location','brand','category','subcategory','productname','descript','model','size','salesprice','sales','created','slug','user','status')
        fields =('picone','pictwo','picthree','picfour','color')