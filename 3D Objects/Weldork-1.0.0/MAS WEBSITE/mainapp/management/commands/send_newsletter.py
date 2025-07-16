from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from mainapp.models import NewsletterSubscription
from django.conf import settings

class Command(BaseCommand):
    help = 'Send a newsletter email to all subscribers.'

    def add_arguments(self, parser):
        parser.add_argument('subject', type=str, help='Subject of the newsletter')
        parser.add_argument('message', type=str, help='Message body (plain text or HTML)')
        parser.add_argument('--html', action='store_true', help='Send as HTML email')

    def handle(self, *args, **options):
        subject = options['subject']
        message = options['message']
        html = options['html']
        emails = list(NewsletterSubscription.objects.values_list('email', flat=True))
        if not emails:
            self.stdout.write(self.style.WARNING('No subscribers found.'))
            return
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
        if html:
            send_mail(subject, '', from_email, emails, html_message=message)
        else:
            send_mail(subject, message, from_email, emails)
        self.stdout.write(self.style.SUCCESS(f'Newsletter sent to {len(emails)} subscribers.'))
