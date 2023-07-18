# RegistrationModelViewSet
from .views import RegistrationModelViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("registration", RegistrationModelViewSet, "register")


urlpatterns = router.urls
