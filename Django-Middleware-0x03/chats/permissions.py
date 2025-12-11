from rest_framework import permissions

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants in a conversation can send, view, update, or delete messages
    """

    def has_permission(self, request, view):
        # ✅ Require authentication globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # ✅ For Conversation objects
        if hasattr(obj, 'participants'):
            # Allow safe methods (GET, HEAD, OPTIONS) if user is participant
            if request.method in permissions.SAFE_METHODS:
                return request.user in obj.participants.all()
            # Restrict modifying methods (PUT, PATCH, DELETE) to participants only
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return request.user in obj.participants.all()
            return request.user in obj.participants.all()

        # ✅ For Message objects
        if hasattr(obj, 'conversation'):
            if request.method in permissions.SAFE_METHODS:
                return request.user in obj.conversation.participants.all()
            if request.method in ['PUT', 'PATCH', 'DELETE']:
                return request.user in obj.conversation.participants.all()
            return request.user in obj.conversation.participants.all()

        return False

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