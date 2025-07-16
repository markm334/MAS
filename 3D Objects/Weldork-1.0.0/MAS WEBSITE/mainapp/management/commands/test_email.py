from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.conf import settings

class Command(BaseCommand):
    help = 'Test email sending with current Django email settings.'

    def add_arguments(self, parser):
        parser.add_argument('--to', type=str, help='Recipient email address', required=True)

    def handle(self, *args, **options):
        to_email = options['to']
        subject = 'Django Email Test'
        message = 'This is a test email from your Django project.'
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', None) or settings.EMAIL_HOST_USER
        self.stdout.write(f'Sending test email to {to_email} from {from_email}...')
        try:
            result = send_mail(subject, message, from_email, [to_email], fail_silently=False)
            if result:
                self.stdout.write(self.style.SUCCESS('Test email sent successfully.'))
            else:
                self.stdout.write(self.style.ERROR('Test email was not sent.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error sending test email: {e}'))
