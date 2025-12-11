# middleware.py
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
handler = logging.FileHandler("request_logs.txt")  # logs will be written here
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


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
