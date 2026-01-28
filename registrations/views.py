from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from events.models import Event

from .models import Registration
from .serializers import RegistrationSerializer


# ===== API VIEWS =====
class RegisterForEventView(generics.CreateAPIView):
    """API: Create registration for an event"""
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Save with current user"""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """Override create to provide custom response"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {
                "detail": "Registration successful",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED
        )


class CancelRegistrationView(APIView):
    """API: Cancel registration for an event"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, event_id):
        """Delete registration"""
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

    def patch(self, request, event_id):
        """Support PATCH method as well (for backward compatibility)"""
        return self.delete(request, event_id)


# ===== HTML VIEWS =====
@login_required
def register_event(request, event_id):
    if request.method == "GET":
        # Telefon yoki noto‘g‘ri ochilish bo‘lsa
        return redirect("/events/")

    event = get_object_or_404(Event, id=event_id)

    Registration.objects.get_or_create(
        user=request.user,
        event=event
    )

    return redirect("/events/")


@login_required
def cancel_registration(request, event_id):
    if request.method == "POST":
        Registration.objects.filter(
            user=request.user,
            event_id=event_id
        ).delete()
    return redirect("/events/")

