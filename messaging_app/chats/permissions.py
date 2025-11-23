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
        # Require authentication globally
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Object-level permissions:
        - For Conversation: user must be a participant
        - For Message: user must be sender or participant in the conversation
        """
        if hasattr(obj, "participants"):  # Conversation instance
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):  # Message instance
            return (
                obj.sender == request.user or
                request.user in obj.conversation.participants.all()
            )

        return False
