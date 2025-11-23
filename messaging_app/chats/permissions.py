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
