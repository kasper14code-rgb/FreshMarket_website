from django import forms

class CheckoutForm(forms.Form):
    #Delivery address
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Street Address'}))
    city = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    postal_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Postal Code'}))

    #Payment Details
    card_name = forms.CharField(max_length=100, label="Name on Card", widget=forms.TextInput(attrs={'placeholder': 'Name on Card'}))
    card_number = forms.CharField(max_length=16, label="Card Number", widget=forms.TextInput(attrs={'placeholder': '16-digit Card Number'}))
    expiry_date = forms.CharField(max_length=5, label="Expiry Date", widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=3, label="CVV", widget=forms.TextInput(attrs={'placeholder': 'CVV'}))