from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from .models import Conversation

User = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    """
    Extend JWTAuthentication if you want to add custom logic,
    e.g., logging, extra claims, or stricter validation.
    """
    def authenticate(self, request):
        # Call parent to validate token
        result = super().authenticate(request)
        if result is None:
            raise AuthenticationFailed("Invalid or missing JWT token")
        return result


def user_in_conversation(user: User, conversation: Conversation) -> bool:
    """
    Utility function: check if a user is a participant in a conversation.
    """
    return conversation.participants.filter(id=user.id).exists()
