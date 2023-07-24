from django.contrib import admin

from .models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_name')

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    
    date_hierarchy = "date_created"
    list_display = (
        "id",
        "name",
        "address",
        "email",
        "mobile",
        "passing_school",
        "attend_reunion",
        "members_attending_event",
        # "event",
        "attendees_names",
        "payment_date",
        "payment_amount",
        "payment_transaction_id",
        "shirt_size",
        "firm_name",
        "date_created",
    )
    list_filter = ("attend_reunion", "payment_date")
    search_fields = ("name",)


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'event', 'registration')
    list_filter = ('event', 'registration')
    search_fields = ('name',)