from rest_framework import serializers
from .models import User, Conversation, Message


# -----------------------------
# User Serializer
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    # Explicit CharField example
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'user_id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'role',
            'created_at',
        ]

    def validate_email(self, value):
        """Custom validation to enforce domain rules."""
        if not value.endswith("@example.com"):
            raise serializers.ValidationError("Email must be from @example.com domain.")
        return value


# -----------------------------
# Message Serializer
# -----------------------------
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    # Computed field example
    preview = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'sender',
            'message_body',
            'sent_at',
            'preview',
        ]

    def get_preview(self, obj):
        """Return first 30 characters of the message body."""
        return obj.message_body[:30] + ("..." if len(obj.message_body) > 30 else "")


# -----------------------------
# Conversation Serializer
# -----------------------------
class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'messages',
            'created_at',
        ]
