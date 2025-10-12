from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from product.models import Product
# Create your models here.

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text= 'Rating from 1 to 5 stars'
    )
    title= models.CharField(max_length=200)
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['product','created_at']),
            models.Index(fields=['is_approved']),
        ]

        def __str__(self):
            return f'{self.name} - {self.product.name} ({self.rating}★)'
