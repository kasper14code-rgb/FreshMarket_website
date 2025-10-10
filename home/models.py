from django.db import models

# Create your models here.
class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, help_yexy='e.g., Happy Customer, Regular Shopper')
    image = models.ImageField(upload_to='testimonials/',blank=True, null=True)
    rating = models.IntegerField(default=5, choices=[(i, f'{i} Stars') for i in range(1,6)])
    comment = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.rating}★'