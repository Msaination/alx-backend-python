from django.db import models

class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a given user.
        Optimized with .only() and select_related.
        """
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .select_related("sender")
            .only("id", "content", "timestamp", "sender")  # 'sender' FK is needed for select_related
        )
