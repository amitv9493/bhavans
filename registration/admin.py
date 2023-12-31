from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import Event, Guest, Payment, Reference, Registration


class ExportResource(resources.ModelResource):
    class Meta:
        model = Payment
        fields = (
            "id",
            "registration",
            "event",
            "payment_date",
            "transaction_id",
        )

    def dehydrate_registration(self, payment):
        return str(payment.registration)

    def dehydrate_event(self, payment):
        return str(payment.event)


class ImportResourse(resources.ModelResource):
    class Meta:
        fields = "__all__"
        model = Payment


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

    search_fields = ("first_name", "last_name", "email", "mobile")


@admin.register(Guest)
class GuestAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "registration")
    list_filter = ("event", "registration")
    search_fields = ("name",)


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    resource_classes = [ImportResourse, ExportResource]

    # def my_receipt(self, obj):
    #     try:
    #         return format_html(
    #             '<img src="{}" style="max-width:200px; max-height:200px"/>'.format(
    #                 obj.receipt.url
    #             )
    #         )
    #     except ValueError:
    #         return

    search_fields = ("registration__first_name", "registration__last_name")
    list_display = ["registration", "receipt", "payment_date"]
    list_filter = ["registration", "payment_date", "event__event_name"]
    list_per_page = 20
    exclude = ("tag",)


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "has_joined"]
