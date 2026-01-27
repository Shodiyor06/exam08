from django.urls import path

from .views import (CancelRegistrationView, RegisterForEventView,
                    cancel_registration, register_event)

urlpatterns = [
    # ===== HTML VIEWS =====
    path("register/<int:event_id>/", register_event, name="register-for-event"),
    path("cancel/<int:event_id>/", cancel_registration, name="cancel-registration"),
    
    # ===== API VIEWS =====
    # POST /api/registrations/register/ - Create registration
    # DELETE /api/registrations/cancel/<event_id>/ - Cancel registration
]