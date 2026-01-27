from.views import EventViewSet, EventRegistrationsCountView, EventAvailableSeatsView, TopEventsByRegistrationsView
from django.urls import path, include
from .views import events_page, add_event

urlpatterns = [
    path("", events_page),
    path("add/", add_event),
    path("registrations-count/<int:event_id>/", EventRegistrationsCountView.as_view()),
    path("available-seats/<int:pk>/", EventAvailableSeatsView.as_view()),
    path("top-registrations/", TopEventsByRegistrationsView.as_view()),
]