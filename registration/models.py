from typing import Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _

import datetime
# Create your models here.

class Event(models.Model):
    event_name = models.CharField(max_length=50)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    event_registration_last_date = models.DateField(default=datetime.date.today)
    
    def __str__(self) -> str:
        return self.event_name
class Registration(models.Model):
    class ChoseEvent(models.TextChoices):
        OPTION1 = "lifetime_membership", "Life Time Membership (INR 2000)"
        OPTION2 = "ex_bhavanites_reunion", "Ex Bhavanites Reunion (INR 7000)"
        OPTION3 = "guest_attending_reunion", "Guest Attending Reunion (INR 5000)"
        OPTION4 = (
            "guest_attending_1st_day",
            "Guest Attending 1st Day Full Function (INR 3500)",
        )
        OPTION5 = (
            "guest_attending_2nd_day",
            "Guest Attending 2nd Day Function (INR 1500)",
        )
        OPTION6 = (
            "guest_attending_gala_dinner",
            "Guest Attending only Gala Dinner (INR 2000)",
        )

    class ProfessionChoice(models.TextChoices):
        option1 = "Businessman", "Businessman"
        option2 = "Entrepreneur", "Entrepreneur"
        option3 = "Doctor", "Doctor"
        option4 = "Lawyer", "Lawyer"
        option5 = "Engineer", "Engineer"
        option6 = "Others", "Others"

    class ShirtSize(models.TextChoices):
        option1 = "XS", "XS"
        option2 = "S", "S"
        option3 = "M", "M"
        option4 = "L", "L"
        option5 = "XL", "XL"
        option6 = "2XL", "2XL"
        option7 = "3XL", "3XL"

    name = models.CharField(max_length=50,null=True, blank=True)
    address = models.TextField()
    email = models.EmailField(max_length=254,null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True, blank=True)
    profession = models.CharField(
        max_length=50,
        choices=ProfessionChoice.choices,
        default=ProfessionChoice.option6,
        null=True, blank=True
    )
    passing_school = models.PositiveSmallIntegerField(
        verbose_name="Year of Passing School",
        null=True, blank=True
    )
    attend_reunion = models.BooleanField(null=True, blank=True)
    members_attending_event = models.PositiveSmallIntegerField(
        verbose_name="Members Attending The Event",
        null=True, blank=True
    )

    event = models.ManyToManyField(Event, related_name="registration", blank=True)
    attendees_names = models.CharField(max_length=255, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.PositiveIntegerField()
    payment_transaction_id = models.CharField(max_length=100, null=True, blank=True)
    shirt_size = models.CharField(
        ("T-shirt Size"), max_length=50, choices=ShirtSize.choices,
        null=True, blank=True
    )

    firm_name = models.CharField(
        _("Name of Firm if Any"), max_length=100, null=True, blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    
    file = models.FileField(upload_to='media', null=True, blank=True)
    
    payment_status = models.BooleanField(default=False)
    # def __str__(self) -> str:
    #     return self.name


