from rest_framework import serializers

from .models import Registration


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializer for Event Registration"""
    
    event_title = serializers.CharField(
        source='event.title',
        read_only=True
    )
    
    class Meta:
        model = Registration
        fields = ("id", "event", "event_title", "registered_at")
        read_only_fields = ("id", "registered_at")

    def validate(self, data):
        """
        Validate registration:
        1. User not already registered for this event
        2. Event has available capacity
        3. Event capacity is greater than 0
        """
        request = self.context.get("request")
        if not request:
            return data
        
        user = request.user
        event = data.get("event")

        if not event:
            raise serializers.ValidationError("Event is required")

        # ===== CHECK 1: User already registered? =====
        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError(
                "Siz bu eventga allaqachon ro'yxatdan o'tgansiz"
            )

        # ===== CHECK 2: Event capacity check =====
        if event.capacity <= 0:
            raise serializers.ValidationError(
                "Bu eventga ro'yxatdan o'tish yopiq (capacity = 0 yoki manfi)"
            )

        # ===== CHECK 3: Check available seats =====
        active_registrations = Registration.objects.filter(event=event).count()
        
        if active_registrations >= event.capacity:
            raise serializers.ValidationError(
                f"Bu eventda bo'sh joy qolmagan ({active_registrations}/{event.capacity} to'lgan)"
            )

        return data