from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer  



# Create your views here.
class ChatListView(APIView):
    def get(self, request):
        # Sample data representing chat messages
        chats = [
            {"id": 1, "message": "Hello!", "sender": "Alice"},
            {"id": 2, "message": "Hi there!", "sender": "Bob"},
        ]
        return Response(chats)

# -----------------------------
# Conversation ViewSet
# -----------------------------
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().order_by('-created_at')
    serializer_class = ConversationSerializer
    permission_classes  = [IsAuthenticated] 
    
    def get_queryset(self):
        # Only return conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expect a list of user_ids in request.data['participants'].
        """
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response(
                {"error": "Participants list is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        users = User.objects.filter(user_id__in=participant_ids)
        conversation.participants.set(users)
        conversation.participants.add(request.user)  # ensure creator is included
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# -----------------------------
# Message ViewSet
# -----------------------------
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('-sent_at')
    serializer_class = MessageSerializer
    
    def get_queryset(self):
        # Only return messages from conversations the user participates in
        return Message.objects.filter(conversation__participants=self.request.user)


    def create(self, request, *args, **kwargs):
        """
        Send a message to an existing conversation.
        Expect 'conversation_id', 'sender_id', and 'message_body' in request.data.
        """
        conversation_id = request.data.get('conversation_id')
        sender_id = request.data.get('sender_id')
        body = request.data.get('message_body')

        if not all([conversation_id, sender_id, body]):
            return Response(
                {"error": "conversation_id, sender_id, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        
        # Ensure user is a participant
        if request.user not in conversation.participants.all():
            return Response({"error": "You are not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)

        message = Message.objects.create(
            conversation=conversation,
            sender=request.user,
            message_body=body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
