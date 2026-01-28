from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from registrations.models import Registration

from .models import Event
from .serializers import EventSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow write access only to admin/staff users"""
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return request.user and request.user.is_staff


class EventViewSet(viewsets.ModelViewSet):
    """API ViewSet for Event CRUD operations"""
    
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        """Set created_by to current user"""
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        """Update event"""
        serializer.save(created_by=self.request.user)


class EventRegistrationsCountView(APIView):
    """Get registration count for an event"""
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        registration_count = event.registrations.count()
        
        return Response({
            "event_id": event.id,
            "title": event.title,
            "registration_count": registration_count
        })


class EventAvailableSeatsView(APIView):
    """Get available seats for an event"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        used = Registration.objects.filter(event=event).count()
        
        # Ensure non-negative available seats
        available = max(0, event.capacity - used)
        
        return Response({
            "event_id": event.id,
            "title": event.title,
            "capacity": event.capacity,
            "registered": used,
            "available_seats": available
        })


class TopEventsByRegistrationsView(APIView):
    """Get top 5 events by registration count"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = (
            Event.objects
            .annotate(registrations_count=Count("registrations"))
            .order_by("-registrations_count")[:5]
        )

        data = [
            {
                "id": e.id,
                "title": e.title,
                "registrations_count": e.registrations_count
            }
            for e in events
        ]

        return Response(data)


# ===== HTML VIEWS =====
@login_required
def events_page(request):
    """Display all events and user's registrations"""
    events = Event.objects.all()

    registered_event_ids = Registration.objects.filter(
        user=request.user
    ).values_list("event_id", flat=True)

    return render(request, "events.html", {
        "events": events,
        "registered_event_ids": registered_event_ids
    })

@@login_required
def add_event(request):
    if request.method == "POST":
        Event.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            event_type=request.POST.get("event_type"),
            location=request.POST.get("location"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time"),
            capacity=request.POST.get("capacity"),
            created_by=request.user,   # 🔥 ENG MUHIM QATOR
        )
        return redirect("/events/")

    return render(request, "templates/add_event.html")

def event_list(request):
    events = Event.objects.all()
    user_regs = []

    if request.user.is_authenticated:
        user_regs = Registration.objects.filter(
            user=request.user
        ).values_list("event_id", flat=True)

    return render(request, "templates/event_list.html", {
        "events": events,
        "user_regs": user_regs,
    })