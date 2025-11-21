# chats/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet
from rest_framework_nested.routers import NestedDefaultRouter


router = rest_framework.routers.DefaultRouter()
router = DefaultRouter() 

router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages", MessageViewSet, basename="message")

# Nested router: messages under conversations
nested_router = NestedDefaultRouter(router, r"conversations", lookup="conversation")
nested_router.register(r"messages", MessageViewSet, basename="conversation-messages")




urlpatterns = [
    path("", include(router.urls)),
    path("", include(nested_router.urls)),
]
