from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMessage
from .models import NewsletterSubscription
# Staff-only newsletter send view
@staff_member_required
def send_newsletter_view(request):
    from .forms import NewsletterSubscriptionForm
    from django import forms
    import logging
    logger = logging.getLogger(__name__)
    class NewsletterSendForm(forms.Form):
        subject = forms.CharField(max_length=200)
        message = forms.CharField(widget=forms.Textarea)
        html = forms.BooleanField(required=False, label='Send as HTML email')
        pdf = forms.FileField(required=False, label='Attach PDF (optional)')

    form = NewsletterSendForm(request.POST or None, request.FILES or None)
    emails = list(NewsletterSubscription.objects.values_list('email', flat=True))
    sent = False
    if request.method == 'POST' and form.is_valid():
        subject = form.cleaned_data['subject']
        message = form.cleaned_data['message']
        html = form.cleaned_data['html']
        pdf = form.cleaned_data['pdf']
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
        logger.info('Sending email: subject=%s, from=%s, to=%s, bcc=%s, html=%s, pdf=%s', subject, from_email, [from_email], emails, html, bool(pdf))
        email = EmailMessage(subject, message, from_email, [from_email], bcc=emails)
        if html:
            email.content_subtype = 'html'
        if pdf:
            logger.info('Attaching PDF: %s', pdf.name)
            email.attach(pdf.name, pdf.read(), pdf.content_type)
        try:
            result = email.send()
            logger.info('Email send result: %s', result)
            sent = True
        except Exception as e:
            logger.error('Error sending email: %s', e, exc_info=True)
            form.add_error(None, f'Error sending newsletter: {e}')
    return render(request, 'send_newsletter_public.html', {'form': form, 'sent': sent, 'subscribers': emails})
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewsletterSubscriptionForm

# ...existing code...

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if not form.Meta.model.objects.filter(email=email).exists():
                form.save()
                messages.success(request, 'Thank you for subscribing!')
            else:
                messages.info(request, 'You are already subscribed.')
        else:
            messages.error(request, 'Please enter a valid email address.')
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')
# Feature detail views
from django.shortcuts import render

def feature_smart_functionality(request):
    return render(request, 'feature_smart_functionality.html')

def feature_eco_friendly_design(request):
    return render(request, 'feature_eco_friendly_design.html')

def feature_energy_efficient(request):
    return render(request, 'feature_energy_efficient.html')

def feature_user_centric(request):
    return render(request, 'feature_user_centric.html')
from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings

def index(request):
    return render(request, 'index.html')

from .forms import NewsletterSubscriptionForm

def about(request):
    form = NewsletterSubscriptionForm()
    return render(request, 'about.html', {'form': form})

def service(request):
    return render(request, 'service.html')

def feature(request):
    return render(request, 'feature.html')

def team(request):
    return render(request, 'team.html')

def testimonial(request):
    return render(request, 'testimonial.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            Contact.objects.create(**form.cleaned_data)
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            mobile = form.cleaned_data.get('mobile')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')
            full_message = f"Name: {name}\nEmail: {email}\nMobile: {mobile}\nSubject: {subject}\nMessage: {message}"
            send_mail(
                subject or 'Contact Form Submission',
                full_message,
                settings.EMAIL_HOST_USER,
                ['ndiatvcict@gmail.com'],
                fail_silently=False,
            )
            return render(request, 'contact.html', {'success': True, 'form': ContactForm()})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def appoinment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        assistive_service = request.POST.get('assistive_service')
        message = request.POST.get('message')
        full_message = f"Name: {name}\nEmail: {email}\nMobile: {mobile}\nService: {assistive_service}\nMessage: {message}"
        send_mail(
            f'Assistive Consultation Request: {assistive_service}',
            full_message,
            settings.EMAIL_HOST_USER,
            ['ndiatvcict@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'appoinment.html', {'success': True})
    return render(request, 'appoinment.html')

def about_html_redirect(request):
    return redirect('about', permanent=True)

def service_html_redirect(request):
    return redirect('service', permanent=True)

def feature_html_redirect(request):
    return redirect('feature', permanent=True)

def team_html_redirect(request):
    return redirect('team', permanent=True)

def testimonial_html_redirect(request):
    return redirect('testimonial', permanent=True)

def appointment_html_redirect(request):
    return redirect('appointment', permanent=True)

def contact_html_redirect(request):
    return redirect('contact', permanent=True)

# Privacy Policy page
def privacy(request):
    return render(request, 'privacy.html')

# Support page
def support(request):
    return render(request, 'support.html')

# Inde page
def inde(request):
    return render(request, 'inde.html')

# Terms and Conditions page
def terms(request):
    return render(request, 'terms.html')
