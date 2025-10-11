from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            
            # Send email to admin
            try:
                send_mail(
                    subject=f'Contact Form: {contact_message.get_subject_display()}',
                    message=f'Name: {contact_message.name}\n'
                            f'Email: {contact_message.email}\n'
                            f'Phone: {contact_message.phone}\n\n'
                            f'Message:\n{contact_message.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                print(f'Email error: {e}')
            
            messages.success(request, 'Thank you for contacting us! We will respond shortly.')
            return redirect('contact:contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    context = {'form': form}
    return render(request, 'contact/contact.html', context)