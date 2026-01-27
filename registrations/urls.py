from django.urls import path
from .views import register_event, cancel_registration 

urlpatterns = [
    path("register/<int:event_id>/", register_event, name="register-for-event"),
    path("cancel/<int:event_id>/", cancel_registration, name="cancel-registration"),
]