from django import forms
from .models import Product,ProductSize,ProductColor


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
        'color':forms.TextInput(attrs={'class':'text-input','placeholder':'product color,exp red'}),
        'productname':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product name'}),
        'model':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product model'}),
        'location':forms.TextInput(attrs={'class':'text-input','placeholder':'Enter product location'}),
        'pdprice':forms.NumberInput(attrs={'class':'text-input','placeholder':'Example "2000" digits only '}),
        }
        exclude=('salesprice','sales','created','slug','user','status')
        fields =('color','pdprice','state','location','brand','category','subcategory','productname','picone','pictwo','picthree','picfour','descript','model','size')

# add product sizes

class Productcolors(forms.ModelForm):
    class Meta:
        model = ProductColor
        widgets={
        'color':forms.TextInput(attrs={'type':'color','class':'text-input','placeholder':'example red'}),

        }
        exclude=('user',)
        fields =('picone','pictwo','picthree','picfour','color')


class ProductSizefm(forms.ModelForm):
    class Meta:
        model= ProductSize
        widgets={
        'sizeprice':forms.NumberInput(attrs={'class':'text-select','placeholder':'product cost for this size if any'}),
        'size':forms.TextInput(attrs={'class':'text-select','placeholder':'exp XL for cloths, 42 for shoes, 32inches for electronics'}),
        }
        exclude=('user','updated ','created')
        fields=('pricechange','sizeprice','size')