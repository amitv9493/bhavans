from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from registration.models import *
import pytz
from datetime import datetime


class Command(BaseCommand):
    help = "Send emails for birthday and anniversary wishes"

    def handle(self, *args, **options):
        current_date = datetime.now(tz=pytz.timezone("Asia/Kolkata"))

        regs = Registration.objects.values("id", "email", "dob", "anniversary_date")
        
        for reg in regs:
            if 
        self.stdout.write(self.style.SUCCESS("Successfully sent emails"))
