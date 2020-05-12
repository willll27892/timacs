from django import forms
from billing.models import Billing

class billingForm(forms.ModelForm):
    class Meta:
        model = Billing
        widgets ={
          'contact':forms.TextInput(attrs={'placeholder':'(areacoder)-your number'}),
          'name':forms.TextInput(attrs={'placeholder':'Your Name'}),
          'address':forms.TextInput(attrs={'placeholder':'Billing Address'}),
          'town':forms.TextInput(attrs={'placeholder':'Town/City'}),
          'region':forms.TextInput(attrs={'placeholder':'State/Region'}),
          'country':forms.TextInput(attrs={'placeholder':'Country'}),
          'billtype':forms.Select(attrs={'placeholder':'Zipecode(Optional)'}),
          'zipcode':forms.TextInput(attrs={'placeholder':'Zipecode(Optional)'}),

        }
        exclude=('owner','created')
        fields=('contact','name','address','town','region','country','billtype','zipcode')