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
    
    queryset = Event.objects.all().order_by('-created_at')
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


@login_required
def add_event(request):
    """Add a new event (admin only)"""
    if not request.user.is_staff:
        return redirect("/events/")
    
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        event_type = request.POST.get("event_type", "ONLINE")
        location = request.POST.get("location", "").strip()
        capacity = request.POST.get("capacity", 0)

        if not title or not capacity:
            render(request, "add_event.html", {
                "error": "Title va capacity majburiy"
            })
            return None

        try:
            capacity = int(capacity)
            if capacity < 0:
                raise ValueError("Capacity manfiy bo'lishi mumkin emas")
        except ValueError:
            return render(request, "add_event.html", {
                "error": "Capacity raqam bo'lishi kerak"
            })

        try:
            Event.objects.create(
                title=title,
                description=description,
                event_type=event_type,
                location=location if event_type == "OFFLINE" else None,
                capacity=capacity,
                created_by=request.user,
                start_time="2026-01-28 10:00:00",
                end_time="2026-01-28 12:00:00"
            )
            return redirect("/events/")
        except Exception as e:
            return render(request, "add_event.html", {
                "error": f"Xatolik: {str(e)}"
            })

    return render(request, "add_event.html")