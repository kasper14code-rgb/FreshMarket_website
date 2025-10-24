from django.db import models
from product.models import Product
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


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

    def get_discounted_price(self, original_price):
        """
        Calculate discounted price for a given product price.
        
        Args:
            original_price: The original price of the product
            
        Returns:
            The discounted price based on deal type
        """
        # Convert to Decimal if not already
        original_price = Decimal(str(original_price))
        
        if self.deal_type == 'percentage' and self.discount_percentage > 0:
            # Convert percentage calculation to Decimal
            percentage = Decimal(str(self.discount_percentage))
            discount_factor = (Decimal('100') - percentage) / Decimal('100')
            discounted = original_price * discount_factor
            return round(discounted, 2)
        elif self.deal_type == 'fixed' and self.discount_amount > 0:
            discounted = original_price - self.discount_amount
            return round(max(discounted, Decimal('0')), 2)
        else:
            return round(original_price, 2)

    @property
    def discounted_price(self):
        """
        Returns discounted price based on discount type.
        Assumes self.original_price is set.
        """
        if self.deal_type == 'percentage' and self.discount_percentage > 0:
            return round(self.original_price * (1 - self.discount_percentage / 100), 2)
        elif self.deal_type == 'fixed' and self.discount_amount > 0:
            discounted = self.original_price - self.discount_amount
            return round(discounted if discounted > 0 else 0, 2)
        else:
            return self.original_price