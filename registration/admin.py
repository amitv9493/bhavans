from django.contrib import admin

from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "event_name")


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "dob",
        "address",
        "country",
        "countryISO",
        "state",
        "stateISO",
        "city",
        "cityISO",
        "anniversary_date",
        "mobile",
        "profession",
        "passing_school",
        "attend_reunion",
        "members_attending_event",
        "shirt_size",
        "firm_name",
        "date_created",
    )
    list_filter = (
        "dob",
        "anniversary_date",
        "attend_reunion",
        "date_created",
    )


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "registration")
    list_filter = ("event", "registration")
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["registration", "payment_success", "payment_amt"]
    list_filter = ["registration"]


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "has_joined"]
