from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    """Event serializer with created_by user info"""
    
    created_by_username = serializers.CharField(
        source='created_by.username', 
        read_only=True
    )
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Event
        fields = (
            "id",
            "title",
            "description",
            "event_type",
            "location",
            "start_time",
            "end_time",
            "capacity",
            "created_by",
            "created_by_username",
            "created_at",
        )
        read_only_fields = ("id", "created_by", "created_at")

    def validate(self, data):
        """Validate start_time and end_time"""
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if start_time and end_time and end_time < start_time:
            raise serializers.ValidationError({
                'end_time': "end_time start_time dan kichik bo'lishi mumkin emas"
            })
        
        return data