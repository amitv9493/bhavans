from io import BytesIO

import xhtml2pdf.pisa as pisa
from django.conf import settings
from django.core.files import File
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags

from .models import Payment


# @receiver(post_save, sender=Registration)
def send_email_on_save(instance, created, *args, **kwargs):
    if created:
        email_subject, from_email, to = (
            "Confirmation Email",
            settings.EMAIL_HOST_USER,
            instance.registration.email,
        )

        guest_list = kwargs.get("guest_list", None)
        print(guest_list)

    event = ", ".join(i.__str__() for i in instance.event.all())
    context = {
        "email": instance.registration.email,
        "date": instance.registration.date_created,
        "payment_date": instance.payment_date,
        "transactionID": instance.razorpay_order_id,
        "event": event,
        "amt": instance.payment_amt,
        "guest_list": guest_list,
    }

    html = get_template("registration/email.html").render(context=context)
    result = BytesIO()
    pdf = pisa.pisaDocument(
        BytesIO(html.encode("UTF-8")),
        result,
    )
    pdf = result.getvalue()
    filename = "receipt" + ".pdf"
    pdf_file = File(BytesIO(pdf), name=filename)

    instance.receipt.save(filename, pdf_file)
    print(
        to,
    )
    email = EmailMultiAlternatives(
        email_subject,
        "receipt generated. Plase find attached with this email",
        from_email,
        [to, "Baavadodara@gmail.com"],
    )

    email.mixed_subtype = "related"

    email.attach(filename, pdf, "application/pdf")
    # email.send(fail_silently=False)


@receiver(post_save, sender=Payment)
def send_email_on_payment_receipt_upload(instance, created, *args, **kwargs):
    if created:
        from_email, to = settings.EMAIL_HOST_USER, instance.registration.email
        context = {
            "event_name": instance.event.event_name,
            "trans_id": instance.transaction_id,
            "amount": instance.event.amount,
            "image_url": instance.receipt.url,
        }
        html_message = render_to_string("registration/payment.html", context=context)
        plain_message = strip_tags(html_message)

        message = EmailMultiAlternatives(
            subject="Thanks for the Payment",
            body=plain_message,
            from_email=from_email,
            to=[to],
        )

        message.attach_alternative(html_message, "text/html")
        message.send()
