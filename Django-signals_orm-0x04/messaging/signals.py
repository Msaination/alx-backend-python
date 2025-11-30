from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Message, MessageHistory

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # only if updating an existing message
        try:
            old_message = Message.objects.get(pk=instance.pk)
        except Message.DoesNotExist:
            return
        if old_message.content != instance.content:
            # Save old content to history
            MessageHistory.objects.create(
                message=old_message,
                old_content=old_message.content
            )
            # Mark message as edited
            instance.edited = True
