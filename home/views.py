from django.shortcuts import render
from product.models import Product
from .models import Testimonial

def index(request):
    bestsellers = Product.objects.filter(is_bestseller=True, is_active=True)[:5]
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    
    context = {
        'bestsellers': bestsellers,
        'testimonials': testimonials,
    }
    return render(request, 'home/index.html', context)