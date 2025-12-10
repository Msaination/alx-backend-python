from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.
class ChatListView(APIView):
    def get(self, request):
        # Sample data representing chat messages
        chats = [
            {"id": 1, "message": "Hello!", "sender": "Alice"},
            {"id": 2, "message": "Hi there!", "sender": "Bob"},
        ]
        return Response(chats)
    
