import logging
from django.contrib import admin
from django.urls import path
from django.template.response import TemplateResponse
from .models import Contact, Newsletter, NewsletterSubscription
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'pdf')
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.shortcuts import render, redirect
from django.urls import path
from .models import NewsletterSubscription

class NewsletterForm(forms.Form):
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)
    html = forms.BooleanField(required=False, label='Send as HTML email')
    pdf = forms.FileField(required=False, label='Attach PDF (optional)')

def send_newsletter(modeladmin, request, queryset):
    from django.core.mail import EmailMessage
    logger = logging.getLogger(__name__)
    emails = list(queryset.values_list('email', flat=True))
    if not emails:
        modeladmin.message_user(request, 'No subscribers selected. Please select at least one subscriber.', level='error')
        return redirect(request.get_full_path())
    if request.method == 'POST':
        form = NewsletterForm(request.POST, request.FILES)
        logger.info('Form submitted. Valid: %s', form.is_valid())
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            html = form.cleaned_data['html']
            pdf = form.cleaned_data['pdf']
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
            logger.info('Sending email: subject=%s, from=%s, to=%s, bcc=%s, html=%s, pdf=%s', subject, from_email, [from_email], emails, html, bool(pdf))
            # Send to first recipient as 'to', rest as BCC for deliverability testing
            if emails:
                to_email = [emails[0]]
                bcc_emails = emails[1:]
            else:
                to_email = [from_email]
                bcc_emails = []
            email = EmailMessage(subject, message, from_email, to_email, bcc=bcc_emails)
            if html:
                email.content_subtype = 'html'
            if pdf:
                logger.info('Attaching PDF: %s', pdf.name)
                email.attach(pdf.name, pdf.read(), pdf.content_type)
            try:
                result = email.send()
                logger.info('Email send result: %s', result)
                if result == 0:
                    logger.error('Django email backend returned 0 (no emails sent).')
                    modeladmin.message_user(request, 'Error: No emails were sent. Please check your email backend configuration and logs.', level='error')
                    return redirect(request.get_full_path())
            except Exception as e:
                import traceback
                tb = traceback.format_exc()
                logger.error('Error sending email: %s\nTraceback:\n%s', e, tb)
                modeladmin.message_user(request, f'Error sending newsletter: {e}', level='error')
                return redirect(request.get_full_path())
            modeladmin.message_user(request, f'Newsletter sent to {len(emails)} subscribers.')
            return redirect(request.get_full_path())
        else:
            logger.warning('Form invalid: %s', form.errors)
            modeladmin.message_user(request, f'Form invalid: {form.errors}', level='error')
    else:
        form = NewsletterForm()
    return render(request, 'admin/send_newsletter.html', {'form': form, 'subscribers': queryset})

send_newsletter.short_description = "Send newsletter to selected subscribers"

from django.utils.html import format_html
from django.urls import reverse

class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')

    change_list_template = 'admin/mainapp/newslettersubscription/change_list.html'

    def changelist_view(self, request, extra_context=None):
        from django.urls import reverse
        url = reverse('send_newsletter_public')
        if extra_context is None:
            extra_context = {}
        extra_context['send_newsletter_link'] = format_html('<a class="button btn btn-primary" href="{}" target="_blank">Send Newsletter to All</a>', url)
        return super().changelist_view(request, extra_context=extra_context)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.actions = [send_newsletter_action]

def send_newsletter_action(modeladmin, request, queryset):
    from django import forms
    from django.core.mail import EmailMessage
    from django.conf import settings
    import logging
    logger = logging.getLogger(__name__)
    class NewsletterSendForm(forms.Form):
        subject = forms.CharField(max_length=200)
        message = forms.CharField(widget=forms.Textarea)
        html = forms.BooleanField(required=False, label='Send as HTML email')
        pdf = forms.FileField(required=False, label='Attach PDF (optional)')

    if 'apply' in request.POST:
        form = NewsletterSendForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            html = form.cleaned_data['html']
            pdf = form.cleaned_data['pdf']
            emails = list(queryset.values_list('email', flat=True))
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
            logger.info('Sending email: subject=%s, from=%s, to=%s, bcc=%s, html=%s, pdf=%s', subject, from_email, [from_email], emails, html, bool(pdf))
            # Send to first recipient as 'to', rest as BCC for deliverability testing
            if emails:
                to_email = [emails[0]]
                bcc_emails = emails[1:]
            else:
                to_email = [from_email]
                bcc_emails = []
            email = EmailMessage(subject, message, from_email, to_email, bcc=bcc_emails)
            if html:
                email.content_subtype = 'html'
            if pdf:
                logger.info('Attaching PDF: %s', pdf.name)
                email.attach(pdf.name, pdf.read(), pdf.content_type)
            try:
                result = email.send()
                logger.info('Email send result: %s', result)
                modeladmin.message_user(request, f'Newsletter sent to {len(emails)} selected subscribers.')
            except Exception as e:
                logger.error('Error sending email: %s', e, exc_info=True)
                modeladmin.message_user(request, f'Error sending newsletter: {e}', level='error')
            return redirect(request.get_full_path())
    else:
        form = NewsletterSendForm()
    return render(request, 'admin/send_newsletter.html', {'form': form, 'subscribers': queryset})

send_newsletter_action.short_description = "Send newsletter to selected subscribers"

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'pdf')

class SendNewsletterAdmin(admin.ModelAdmin):
    change_list_template = 'admin/send_newsletter.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-newsletter/', self.admin_site.admin_view(self.send_newsletter_view), name='send-newsletter'),
        ]
        return custom_urls + urls

    def send_newsletter_view(self, request):
        import logging
        from django.core.mail import EmailMessage
        logger = logging.getLogger(__name__)
        form = NewsletterForm(request.POST or None, request.FILES or None)
        emails = list(NewsletterSubscription.objects.values_list('email', flat=True))
        if request.method == 'POST' and form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            html = form.cleaned_data['html']
            pdf = form.cleaned_data['pdf']
            from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
            logger.info('Sending email: subject=%s, from=%s, to=%s, bcc=%s, html=%s, pdf=%s', subject, from_email, [from_email], emails, html, bool(pdf))
            # Send to first recipient as 'to', rest as BCC for deliverability testing
            if emails:
                to_email = [emails[0]]
                bcc_emails = emails[1:]
            else:
                to_email = [from_email]
                bcc_emails = []
            email = EmailMessage(subject, message, from_email, to_email, bcc=bcc_emails)
            if html:
                email.content_subtype = 'html'
            if pdf:
                logger.info('Attaching PDF: %s', pdf.name)
                email.attach(pdf.name, pdf.read(), pdf.content_type)
            try:
                result = email.send()
                logger.info('Email send result: %s', result)
                self.message_user(request, f'Newsletter sent to {len(emails)} subscribers.')
            except Exception as e:
                logger.error('Error sending email: %s', e, exc_info=True)
                self.message_user(request, f'Error sending newsletter: {e}', level='error')
        context = dict(
            self.admin_site.each_context(request),
            form=form,
            subscribers=NewsletterSubscription.objects.all(),
        )
        return TemplateResponse(request, 'admin/send_newsletter.html', context)

admin.site.register(Contact)
admin.site.register(NewsletterSubscription, NewsletterSubscriptionAdmin)
