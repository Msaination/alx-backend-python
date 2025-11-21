# chats/urls.py
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = DefaultRouter()
router.register(r"api/v1/conversations", ConversationViewSet, basename="conversation")
router.register(r"api/v1/messages", MessageViewSet, basename="message")

urlpatterns = router.urls
