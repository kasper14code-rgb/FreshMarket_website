from django.db import models
from product.models import Product 

class Review(models.Model):
    RATING_CHOICES = [
        (0, '1 Star'),
        (1, '2 Stars'),
        (2, '3 Stars'),
        (3, '4 Stars'),
        (4, '5 Stars'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews',null=True,blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    rating = models.IntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Add auto_now=True
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"