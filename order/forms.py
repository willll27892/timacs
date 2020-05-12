from django import forms
from .models import ReceiversName

class ReceiverInfo(forms.ModelForm):
    class Meta:
        model=ReceiversName
        widgets={
            'name':forms.TextInput(attrs={'class':'input-text'}),
            'contact':forms.NumberInput(attrs={'class':'input-text'}),
        }
        exclude=('session','created')
        fields=('name','contact')
