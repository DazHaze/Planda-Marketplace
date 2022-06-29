from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    sale_products = Product.objects.filter(on_sale=True)

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'
        

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'sale_products': sale_products,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def sale_products(request):
    """ A view to show all sale products """
    items = Product.objects.filter(on_sale=True)

    context = {'items': items}

    return render(request, 'products/sale_products.html', context)




def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)

@login_required
def favourite_add(request, favourite_id):
    """ A view to add a favourite product """
    fav_product = get_object_or_404(Product, id=favourite_id)
    if fav_product.favourites.filter(id=request.user.id).exists():
        fav_product.favourites.remove(request.user)
    else:
        fav_product.favourites.add(request.user)
    context = {
    'product': fav_product,
    }
    return render(request, 'products/product_detail.html', context)
    # return HttpResponseRedirect(request.META['HTTP_REFERER'])
