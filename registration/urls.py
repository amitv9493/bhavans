# RegistrationModelViewSet
from .views import *
from rest_framework.routers import DefaultRouter
from django.urls import path

router = DefaultRouter()

router.register("registration", RegistrationModelViewSet, "register")


urlpatterns = [
    path("email/", email),
    path(
        "create/order/",
        getOrderCreated,
    ),
    # path("create/",RegistrationCreateView.as_view()),
    path("get/current-events/", EventGETView.as_view()),
    path("payment/<int:registration_id>/", Payment, name="payment"),
    path("payment/complete/", PaymentView.as_view()),
    path("refer/", ReferenceCreateView),
    path("refer/<int:pk>/", ReferenceGETView),
    path("custom-users/<int:year>/",UserView,name="customUsers"),

] + router.urls
