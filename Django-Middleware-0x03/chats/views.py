from rest_framework import viewsets, permissions, filters, status
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipant, IsMessageOwnerOrParticipant
from rest_framework.response import Response
from .auth import CustomJWTAuthentication
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User 



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    
  
    authentication_classes = [CustomJWTAuthentication]
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, filters.DjangoFilterBackend]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]


    # filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ["participants__email"]   # search by participant email
    ordering_fields = ["created_at"]
    
    def get_queryset(self):
        # Only conversations where the user is a participant
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.save()
        conversation.participants.add(self.request.user)
        return conversation
    
    def add_participant(self, request, pk=None):
        conversation = self.get_object()
        user_id = request.data.get("user_id")
        try:
            user = User.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({"status": "participant added"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    authentication_classes = [CustomJWTAuthentication]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = MessageFilter
    search_fields = ["message_body", "sender__email"]
    ordering_fields = ["sent_at"]
    
    
    def get_queryset(self):
        # Only messages in conversations where the user is a participant
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        Conversation_id = self.request.data.get("conversation_id")
        try:
            conversation = Conversation.objects.get(id=Conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save(sender=self.request.user, conversation=conversation)
         
        
