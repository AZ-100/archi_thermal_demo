# your_app/context_processors.py
from .models import Product
from collections import defaultdict

def products_context(request):
    products = Product.objects.all()  # Fetch all products
    products_by_type = defaultdict(list)

    # Group products by type
    for product in products:
        products_by_type[product.product_type].append(product)

    return {
        'products_by_type': products_by_type,
    }
