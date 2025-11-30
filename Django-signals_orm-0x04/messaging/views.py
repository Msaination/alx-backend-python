from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Message, Notification
from .utils import get_thread  # recursive helper for threaded conversations


@login_required
def delete_user(request):
    user = request.user
    user.delete()  # triggers post_delete signal
    return redirect('home')  # redirect to homepage after deletion

@login_required
def notifications_view(request):
    """
    Fetch all notifications for the logged-in user.
    """
    notifications = Notification.objects.filter(user=request.user).select_related("message")
    data = [
        {
            "id": n.id,
            "message_id": n.message.id,
            "message_content": n.message.content,
            "created_at": n.created_at,
            "is_read": n.is_read,
        }
        for n in notifications
    ]
    return JsonResponse(data, safe=False)

@login_required
def conversation_view(request, message_id):
    """
    Fetch a root message and its immediate replies (non-recursive).
    Optimized with select_related and prefetch_related.
    """
    root_message = get_object_or_404(
        Message.objects.select_related("sender", "receiver"),
        pk=message_id
    )
    replies = root_message.replies.prefetch_related("sender", "receiver")

    data = {
        "root": {
            "id": root_message.id,
            "content": root_message.content,
            "sender": root_message.sender.username,
            "receiver": root_message.receiver.username,
        },
        "replies": [
            {
                "id": r.id,
                "content": r.content,
                "sender": r.sender.username,
                "receiver": r.receiver.username,
            }
            for r in replies
        ]
    }
    return JsonResponse(data)


@login_required
def threaded_conversation_view(request, message_id):
    """
    Fetch a root message and all its replies recursively.
    Returns a nested JSON structure for threaded conversations.
    """
    root_message = get_object_or_404(
        Message.objects.select_related("sender", "receiver"),
        pk=message_id
    )
    thread = get_thread(root_message)
    return JsonResponse(thread, safe=False)
