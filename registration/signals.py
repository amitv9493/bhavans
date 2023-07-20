from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from .models import Registration, Event
from django.conf import settings
from django.template.loader import render_to_string, get_template
from django.conf import settings
from django.db import transaction
from io import BytesIO
import xhtml2pdf.pisa as pisa
from django.conf import settings


from django.core.exceptions import ValidationError


# @receiver(post_save, sender=Registration)
@receiver(m2m_changed, sender=Registration.event.through)
def send_email_on_save(sender, instance, action, **kwargs):
    # if created:
    if action == 'post_add':
        email_subject, from_email, to = (
            "Confirmation Email",
            settings.EMAIL_HOST_USER,
            instance.email,
        )
        
        events = list(Event.objects.filter(registration= instance.id).values_list("event_name", flat=True))
        # print(events)
        
        # print([i.event_name for i in instance.regis])
        context = {
            "payment_date": instance.payment_date,
            "amt": instance.payment_amount,
            "email": instance.email,
            "transactionID": instance.payment_transaction_id,
            "event": events,
            "date": instance.date_created,
        }

        html = get_template("registration/email.html").render(context=context)
        result = BytesIO()
        pdf = pisa.pisaDocument(
            BytesIO(html.encode("UTF-8")),
            result,
        )
        pdf = result.getvalue()
        filename = "receipt"+".pdf"

        email = EmailMultiAlternatives(
            email_subject,
            "receipt generated. Plase find attached with this email",
            from_email,
            [to],
        )

        email.mixed_subtype = "related"
        # img_dir = os.path.join(settings.REAL_BASE_DIR, "static", "logo.jpeg")

        # # file_path = os.path.join(img_dir)
        # image = "logo.jpeg"
        # with open(img_dir, "rb") as f:
        #     img = MIMEImage(f.read())
        #     img.add_header("Content-ID", "<{name}>".format(name=image))
        #     img.add_header("Content-Disposition", "inline", filename=image)

        # email.attach(img)

        # EmailThread(email).start()

        # email.attach_alternative(html, "text/html")
        email.attach(filename, pdf, "application/pdf")
        # try:
            # with transaction.atomic():
        email.send(fail_silently=False)
        # instance.save()
        # except Exception as e:
            # raise ValidationError("Error sending email. Please try again later.")
