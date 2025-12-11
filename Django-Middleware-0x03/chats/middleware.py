# middleware.py
import logging
from datetime import datetime
from django.http import HttpResponseForbidden


logger = logging.getLogger(__name__)

handler = logging.FileHandler("requests.log")  # logs will be written here
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server hour (24-hour format)
        current_hour = datetime.now().hour

        # Restrict access outside 6AM–9PM
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden(
                "Access to the messaging app is restricted between 9PM and 6AM."
            )

        # Continue processing request
        response = self.get_response(request)
        return response


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get user info (Anonymous if not logged in)
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log timestamp, user, and path
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_entry)

        # Continue processing request
        response = self.get_response(request)
        return response
