from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg, Max
from .models import Review
from .forms import ReviewForm

def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.is_approved = True
            review.save()
            messages.success(request, "Thank you! Your review has been submitted successfully.")
            return redirect('home:index')
    else:
        form = ReviewForm()
    
    # Get all approved reviews first (without slicing)
    approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    
    # Calculate statistics
    total_reviews = approved_reviews.count()
    
    if total_reviews > 0:
        highest_rating = approved_reviews.aggregate(Max('rating'))['rating__max']
        average_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg']
        positive_reviews = approved_reviews.filter(rating__gte=4).count()
        positive_percentage = round((positive_reviews / total_reviews) * 100)
    else:
        highest_rating = 0
        average_rating = 0
        positive_percentage = 0
    
    # Now slice for display (only the first 10 reviews)
    reviews = approved_reviews[:10]
    
    context = {
        'form': form,
        'reviews': reviews,
        'total_reviews': total_reviews,
        'highest_rating': highest_rating,
        'average_rating': round(average_rating, 1),
        'positive_percentage': positive_percentage,
    }
    
    return render(request, 'reviews/add_review.html', context)

def review_list(request):
    approved_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    
    total_reviews = approved_reviews.count()
    
    if total_reviews > 0:
        average_rating = approved_reviews.aggregate(Avg('rating'))['rating__avg']
        positive_reviews = approved_reviews.filter(rating__gte=4).count()
        positive_percentage = round((positive_reviews / total_reviews) * 100)
    else:
        average_rating = 0
        positive_percentage = 0
    
    context = {
        'reviews': approved_reviews,
        'total_reviews': total_reviews,
        'average_rating': round(average_rating, 1),
        'positive_percentage': positive_percentage,
    }
    
    return render(request, 'reviews/review_list.html', context)