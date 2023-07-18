from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Registration


@receiver(post_save, sender=Registration)
def send_email_on_save(sender, instance, created, **kwargs):
    if created:
        # Logic to send the email
        send_mail(
            "Object Saved",
            "An object has been saved.",
            "sender@example.com",
            ["recipient@example.com"],
            fail_silently=False,
        )
