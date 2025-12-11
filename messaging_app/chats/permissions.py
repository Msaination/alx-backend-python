from rest_framework import permissions


class IsParticipant(permissions.BasePermission):
    """
    Custom permission: only allow participants of a conversation
    to view or send messages in it.
    """

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()

        # For Message objects
        if hasattr(obj, 'conversation'):
            return request.user in obj.conversation.participants.all()

        return False
class IsSender(permissions.BasePermission):
    """
    Custom permission: only allow the sender of a message
    to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # For Message objects
        if hasattr(obj, 'sender'):
            return request.user == obj.sender

        return False        