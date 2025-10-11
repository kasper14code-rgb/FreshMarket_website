# contact/forms.py
from django import forms
from .models import ContactMessage
from django.core.exceptions import ValidationError
import re

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'your.email@example.com',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number (optional)'
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your message...',
                'rows': 6,
                'required': True
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove spaces and dashes
            phone = phone.replace(' ', '').replace('-', '')
            if not re.match(r'^\+?1?\d{9,15}$', phone):
                raise ValidationError('Please enter a valid phone number.')
        return phone

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 20:
            raise ValidationError('Message must be at least 20 characters long.')
        return message
