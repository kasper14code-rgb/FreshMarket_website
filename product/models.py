from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from django.urls import reverse
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100 , unique = True)
    slug = models.SlugField(max_length=100, unique= True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to= 'categories/', blank=True, null= True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    UNIT_CHOICES =[
        ('lb','per lb'),
        ('kg','per kg'),
        ('pcs','per piece'),
        ('bag','per bag'),
        ('box','per box'),
        ('gallon','per gallon'),
        ('liter','per liter'),
        ('dozen','per dozen'),
        ('loaf','per loaf'),
        ('block','per block'),
        ('cup','per cup'),
        ('slice','per slice'),
        ('','each'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='')
    image = models.ImageField(upload_to='product/')
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    is_bestseller = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['is_bestseller']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_detail', kwargs={'slug': self.slug})

    def get_average_rating(self):
        from reviews.models import Review
        reviews = Review.objects.filter(product=self, is_approved=True)
        if reviews.exists():
            return round(reviews.aggregate(models.Avg('rating'))['rating__avg'], 1)
        return 0

    def get_review_count(self):
        from reviews.models import Review
        return Review.objects.filter(product=self, is_approved=True).count()
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"