from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Registration
from .serializers import RegistrationSerializer
from events.models import Event
from django.contrib.auth.decorators import login_required
from events.models import Event

class RegisterForEventView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CancelRegistrationView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, event_id):
        registration = get_object_or_404(
            Registration,
            user=request.user,
            event_id=event_id,
        )

        registration.delete()

        return Response(
            {"detail": "Registration bekor qilindi"},
            status=status.HTTP_200_OK
        )



@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    Registration.objects.get_or_create(
        user=request.user,
        event=event
    )

    return redirect("/events/")


@login_required
def cancel_registration(request, event_id):
    Registration.objects.filter(
        user=request.user,
        event_id=event_id
    ).delete()

    return redirect("/events/")
