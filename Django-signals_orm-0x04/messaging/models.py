from django.db import models
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return unread messages for a given user.
        Optimized with .only() to fetch minimal fields.
        """
        return (
            super().get_queryset()
            .filter(receiver=user, read=False)
            .select_related("sender")  # optimize sender lookups
            .only("id", "content", "timestamp", "sender__username")  # fetch only needed fields
        )


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited_by = models.BooleanField(default=False)  # track edits
    read = models.BooleanField(default=False)  # new field to track read status
    
    # Self-referential FK for threaded replies
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies"
    )
    
    objects = models.Manager()  # default manager
    unread_messages = UnreadMessagesManager()  # custom manager for unread messages 
    


    def __str__(self):
        return f"From {self.sender} to {self.receiver} at {self.timestamp}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="notifications")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - Message {self.message.id}"
    
class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message {self.message.id} at {self.edited_at}"


