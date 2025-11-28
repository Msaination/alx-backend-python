from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Custom permission: only allow participants of a chat to view it.
    """

    def has_object_permission(self, request, view, obj):
        # obj will be a Chat instance
        return request.user in obj.participants.all()


class IsMessageOwnerOrParticipant(permissions.BasePermission):
    """
    Custom permission: only allow sender or chat participants to view a message.
    """

    def has_object_permission(self, request, view, obj):
        # obj will be a Message instance
        return (
            obj.sender == request.user or
            request.user in obj.chat.participants.all()
        )

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API
    - Only participants in a conversation can send, view, update, or delete messages
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Handle Conversation objects
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # Handle Message objects
        if hasattr(obj, "conversation"):
            is_participant = request.user in obj.conversation.participants.all()
            is_sender = obj.sender == request.user

            # Allow GET for participants
            if request.method in permissions.SAFE_METHODS:
                return is_participant or is_sender

            # Allow PUT, PATCH, DELETE only if participant or sender
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return is_participant or is_sender

        return False

