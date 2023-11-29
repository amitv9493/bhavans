from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin

from .models import Event, Guest, Payment, Reference, Registration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "event_name")


@admin.register(Registration)
class RegistrationAdmin(ImportExportModelAdmin):
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
        "date",
        "voucher_no",
        "barcode",
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
    def my_receipt(self, obj):
        try:
            return format_html(
                '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(
                    obj.receipt.url
                )
            )
        except ValueError:
            return

    search_fields = ()
    list_display = ["registration", "my_receipt", "payment_date"]
    list_filter = ["registration", "payment_date", "event__event_name"]
    list_per_page = 20
    exclude = ("tag",)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "has_joined"]
