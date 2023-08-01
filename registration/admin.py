from django.contrib import admin

from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "event_name")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    date_hierarchy = "date_created"
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "mobile",
        "passing_school",
        "attend_reunion",
        # "event",
        "shirt_size",
        "firm_name",
        "date_created",
    )
    list_filter = ("attend_reunion",)
    search_fields = ("name",)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "registration")
    list_filter = ("event", "registration")
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["registration", "payment_success", "payment_amt"]
