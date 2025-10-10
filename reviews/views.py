from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ReviewForm
from product.models import Product

def add_review(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.save()
            
            # Send email notification to admin
            try:
                send_mail(
                    subject=f'New Review for {product.name}',
                    message=f'A new review has been submitted by {review.name}.\n\n'
                            f'Product: {product.name}\n'
                            f'Rating: {review.rating} stars\n'
                            f'Title: {review.title}\n\n'
                            f'Please review and approve it in the admin panel.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f'Email error: {e}')
            
            messages.success(request, 'Thank you! Your review has been submitted and is awaiting approval.')
            return redirect('product:product_detail', slug=product_slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'reviews/add_review.html', context)