from django.shortcuts import render
from products.models import Product

# Create your views here.
def view_favourites(request):
    """ A view to return the users favourite products """
    
    return render(request, 'favourites/favourites.html')