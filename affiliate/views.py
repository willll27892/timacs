from django.shortcuts import render
from affiliate.models import Application
from .forms import AffiliateForm

# Create your views here.

def Apply(request):
    form = AffiliateForm(request.POST or None)
    if request.is_ajax:
        if form.is_valid:
            print('valided')
            instance= form.save(commit=False)
            instance.save()
    context={'form':form}
    template_name="affiliates/homepage.html"
    return render(request,template_name,context)
    