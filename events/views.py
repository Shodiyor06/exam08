from django.db.models import Count
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions
from .models import Event
from .serializers import EventSerializer
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from registrations.models import Registration
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_staff
    


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-created_at')
    serializer_class = EventSerializer
    permissions_classes = [IsAdminOrReadOnly]

    def perfom_create(self, serializer):
        serializer.save(created_by=self.request.user)    

class EventRegistrationsCountView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        registration_count = event.registrations.count()
        return Response({"registration_count": registration_count})
    
class EventAvailableSeatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        used = Registration.objects.filter(event=event).count()

        return Response({
            "event_id": event.id,
            "available_seats": event.capacity - used
        })



class TopEventsByRegistrationsView(APIView):
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
    
@login_required
def events_page(request):
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
    if request.method == "POST":
        title = request.POST.get("title")
        capacity = request.POST.get("capacity")

        if title and capacity:
            Event.objects.create(
                title=title,
                capacity=capacity
            )
            return redirect("/events/")

    return render(request, "add_event.html")
