from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        When creating a conversation, automatically add the requesting user
        as a participant.
        """
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return conversation

    @action(detail=True, methods=["post"])
    def add_participant(self, request, pk=None):
        """
        Custom endpoint: add another user to the conversation.
        """
        conversation = self.get_object()
        user_id = request.data.get("user_id")
        if user_id:
            conversation.participants.add(user_id)
        return Response({"status": "participant added"})

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        When creating a message, set the sender to the requesting user.
        """
        serializer.save(sender=self.request.user)       
        
        
# --- IGNORE ---
