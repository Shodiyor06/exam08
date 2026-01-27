from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (EventAvailableSeatsView, EventRegistrationsCountView,
                    EventViewSet, TopEventsByRegistrationsView, add_event,
                    event_list)

# ===== ROUTER FOR ViewSet =====
router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')

urlpatterns = [
    # HTML views
    path("", event_list, name='events-page'),
    path("add/", add_event, name='add-event'),
    
    # API custom endpoints
    path("<int:event_id>/registrations-count/",
         EventRegistrationsCountView.as_view(),
         name='registrations-count'),
    path("<int:pk>/available-seats/",
         EventAvailableSeatsView.as_view(),
         name='available-seats'),
    path("top-registrations/",
         TopEventsByRegistrationsView.as_view(),
         name='top-registrations'),
]
urlpatterns += router.urls