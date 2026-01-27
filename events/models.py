from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Event(models.Model):
    EVENT_TYPE_CHOICES = (
        ("ONLINE", "Online"),
        ("OFFLINE", "Offline"),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(
        max_length=10,
        choices=EVENT_TYPE_CHOICES
    )
    location = models.CharField(max_length=255, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    capacity = models.IntegerField(default=1)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def clean(self):
        """Validate model fields"""
        errors = {}

        # Capacity validation
        if self.capacity < 0:
            errors['capacity'] = "Capacity manfiy bo'lishi mumkin emas"

        # Time validation
        if self.end_time and self.start_time:
            if self.end_time < self.start_time:
                errors['end_time'] = "end_time start_time dan kichik bo'lishi mumkin emas"

        # Offline event must have location
        if self.event_type == "OFFLINE" and not self.location:
            errors['location'] = "Offline event uchun location kiritish shart"

        if errors:
            raise ValidationError(errors)

        # Online events don't need location
        if self.event_type == "ONLINE":
            self.location = None

    def save(self, *args, **kwargs):
        """Call clean() before saving"""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def available_seats(self):
        """Calculate available seats"""
        from registrations.models import Registration
        used = Registration.objects.filter(event=self).count()
        return max(0, self.capacity - used)

    @property
    def is_full(self):
        """Check if event is full"""
        return self.available_seats == 0