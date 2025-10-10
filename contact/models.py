from django.db import models

# Create your models here.
class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('general','General Inquiry'),
        ('order','Order Issue'),
        ('product','Product Question'),
        ('feedback','Feedback'),
        ('other','Other'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone= models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

        def __str__(self):
            return f'{self.name} - {self.subject} ({self.created_at.strftime("%Y-%m-%d")})'