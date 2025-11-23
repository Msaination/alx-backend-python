import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    # Filter by participant user ID
    participant = django_filters.NumberFilter(
        field_name="conversation__participants__id", lookup_expr="exact"
    )

    # Filter by time range
    start_time = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="gte"
    )
    end_time = django_filters.DateTimeFilter(
        field_name="timestamp", lookup_expr="lte"
    )

    class Meta:
        model = Message
        fields = ["participant", "start_time", "end_time"]

