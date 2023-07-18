from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Registration(models.Model):
    class ChoseEvent(models.TextChoices):
        option1 = 1, "Life Time Membership INR 2000"
        option2 = 2, "Ex Bhavanites Reunion INR 7000"
        option3 = 3, "Guest Attending Reunion INR 5000"
        option4 = 4, "Guest Attending 1st Day Full Fuction INR 3500"
        option5 = 5, "Guest Attending 2nd Day Fuction INR 1500"
        option6 = 6, "Guest Attending only Gala Dinner INR 2000"

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

    name = models.CharField(max_length=50)
    address = models.TextField()
    email = models.EmailField(max_length=254)
    mobile = models.CharField(max_length=10)
    passing_school = models.PositiveSmallIntegerField(
        verbose_name="Year of Passing School"
    )
    attend_reunion = models.BooleanField()
    members_attending_event = models.PositiveSmallIntegerField(
        verbose_name="Members Attending The Event",
    )

    event = models.CharField(max_length=1, choices=ChoseEvent.choices)
    attendees_names = models.CharField(max_length=255)
    payment_date = models.DateField()
    payment_amount = models.PositiveIntegerField()
    payment_transaction_id = models.CharField(max_length=100)
    shirt_size = models.CharField(
        ("T-shirt Size"), max_length=50, choices=ShirtSize.choices
    )

    firm_name = models.CharField(
        _("Name of Firm if Any"), max_length=100, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.name
