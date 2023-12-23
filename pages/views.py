from django.shortcuts import render 
from store.models import Product


# Create your views here.
def index(request):
    products = Product.objects.all()
    context = {
        'page_title': 'Home Page',
        'products': products,
    }
    return render(request, 'pages/index.html', context)