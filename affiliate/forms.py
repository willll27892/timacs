from django import forms
from .models import Application

class AffiliateForm(forms.ModelForm):
    class Meta:
        model= Application

        widgets={

        }
        exclude=('created','user')
        fields =('email','name','number','address','occupation')