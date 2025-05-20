from django.http import HttpResponse
from django.shortcuts import render
from .models import Item
from django.template import loader

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def home(request):
    item_list=Item.objects.all()
    template=loader.get_template('food/home.html')
    context={
        'items':item_list
    }
    return render(request,'food/home.html',context)