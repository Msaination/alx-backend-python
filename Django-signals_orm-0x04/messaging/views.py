from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    user.delete()  # triggers post_delete signal
    return redirect('home')  # redirect to homepage after deletion
