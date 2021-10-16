from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_verification_email(data):
        
        
        email = EmailMessage(subject=data['email_subject'],
                             body=data['email_body'],
                             from_email='no-reply@eventara.id',
                             to=data['email_to'])

        email.content_subtype = 'html'
                             
        email.send()
        