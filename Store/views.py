from django.shortcuts import render, get_object_or_404
from .models import Product

# Create your views here.


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def product_list(request):
    products = Product.objects.all()
    return render(request, 'Store/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Store/product_detail.html', {'product': product})


