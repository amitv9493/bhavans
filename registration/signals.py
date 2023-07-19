from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Registration
from django.conf import settings
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction
from io import BytesIO
import xhtml2pdf.pisa as pisa

from django.core.exceptions import ValidationError


@receiver(post_save, sender=Registration)
def send_email_on_save(sender, instance, created, **kwargs):
    if created:
        email_subject, from_email, to = (
            "Confirmation Email",
            settings.EMAIL_HOST_USER,
            instance.email,
        )

        context = {
            "amt": instance.payment_amount,
            "email": instance.email,
            "transactionID": instance.payment_transaction_id,
            "event": instance.event,
        }

        html = render_to_string("registration/email.html", context=context)
        result = BytesIO()

        pdf = pisa.pisaDocument(
            BytesIO(html.encode("UTF-8")),
            result,
        )
        pdf = result.getvalue()
        filename = "receipt" + context["transactionID"] + ".pdf"

        email = EmailMultiAlternatives(
            email_subject,
            html,
            from_email,
            [to],
        )

        email.attach_alternative(html, "text/html")
        email.attach(filename, pdf, "application/pdf")
        try:
            with transaction.atomic():
                email.send(fail_silently=False)
                instance.save()
        except Exception as e:
            raise ValidationError("Error sending email. Please try again later.")
