# Newsletter subscription form
from django import forms
from .models import NewsletterSubscription

class NewsletterSubscriptionForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscription
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control border-0 bg-light',
                'placeholder': 'Your Email',
                'id': 'mail',
            })
        }
from django import forms

# Example form for contact page
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    mobile = forms.CharField(max_length=20, required=False)
    subject = forms.CharField(max_length=200, required=False)
    message = forms.CharField(widget=forms.Textarea)
