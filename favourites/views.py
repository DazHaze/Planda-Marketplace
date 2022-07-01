from django.shortcuts import redirect, get_object_or_404, render
from products.views import product_detail
from products.models import Product
from django.contrib.auth.models import User



# Create your views here.
def view_favourites(request):
    """ A view to return the users favourite products """

    user = request.user
    favourite_products = user.favourites.all()

    context = {
        'favourite_products': favourite_products,
    }
    return render(request, 'favourites/favourites.html', context)


def favourite_product(request, id):
    """ A view to add a product to the users favourite products"""

    product = get_object_or_404(Product, id=id)
    if product.favourites.filter(id=request.user.id).exists():
        product.favourites.remove(request.user)
    else:
        product.favourites.add(request.user)

    return redirect('view_favourites')