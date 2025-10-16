from django.db import models
from product.models import Product
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


class Deal(models.Model):
    """Special deals and promotions"""
    
    DEAL_TYPE_CHOICES = [
        ('percentage', 'Percentage Discount'),
        ('fixed', 'Fixed Amount Off'),
        ('bogo', 'Buy One Get One'),
        ('bundle', 'Bundle Deal'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    deal_type = models.CharField(max_length=20, choices=DEAL_TYPE_CHOICES, default='percentage')
    discount_percentage = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text='Percentage discount (0-100)'
    )
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text='Fixed amount discount'
    )
    products = models.ManyToManyField(Product, related_name='deals')
    banner_image = models.ImageField(upload_to='deals/', blank=True, null=True)
    
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False, help_text='Show on homepage')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def is_valid(self):
        """Check if deal is currently valid"""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date
    
    def get_discount_display(self):
        """Return formatted discount string"""
        if self.deal_type == 'percentage':
            return f"{self.discount_percentage}% OFF"
        elif self.deal_type == 'fixed':
            return f"${self.discount_amount} OFF"
        elif self.deal_type == 'bogo':
            return "BOGO"
        else:
            return "Special Deal"
