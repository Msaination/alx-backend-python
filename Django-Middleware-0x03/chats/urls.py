from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework import routers
from .views import ChatListView, ConversationViewSet, MessageViewSet
from rest_framework_nested import routers
from rest_framework.permissions import IsAuthenticated




router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')    

router.register(r'messages', MessageViewSet, basename='message')


urlpatterns = router.urls + conversations_router.urls
