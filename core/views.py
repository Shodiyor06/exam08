from django.db.models import Count
from django.shortcuts import render

from events.models import Event
from registrations.models import Registration


def login_page(request):
    return render(request, "login.html")

def events_page(request):
    return render(request, "events.html")
def events_static(request):
    return render(request, "stats.html")

def stats_page(request):
    registrations_count = None
    free_places = None
    top_events = []

    event_id = request.GET.get("event_id")

    if event_id:
        registrations_count = Registration.objects.filter(
            event_id=event_id
        ).count()

        event = Event.objects.filter(id=event_id).first()
        if event:
            free_places = event.capacity - registrations_count

    top_events = Event.objects.annotate(
        reg_count=Count("registrations")
    ).order_by("-reg_count")[:5]

    return render(request, "stats.html", {
        "registrations_count": registrations_count,
        "free_places": free_places,
        "top_events": top_events
    })
