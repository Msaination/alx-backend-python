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

class OffensiveLanguageMiddleware:
    """
    Middleware that limits the number of POST requests (messages)
    from each IP address to 5 per minute.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track requests per IP
        # Format: { ip: [timestamps] }
        self.ip_requests = {}

    def __call__(self, request):
        # Only enforce on POST requests (sending messages)
        if request.method == "POST" and "/api/messages" in request.path:
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize list if IP not tracked yet
            if ip not in self.ip_requests:
                self.ip_requests[ip] = []

            # Remove timestamps older than 1 minute
            one_minute_ago = now - timedelta(minutes=1)
            self.ip_requests[ip] = [
                ts for ts in self.ip_requests[ip] if ts > one_minute_ago
            ]

            # Check if limit exceeded
            if len(self.ip_requests[ip]) >= 5:
                return HttpResponseForbidden(
                    "Rate limit exceeded: You can only send 5 messages per minute."
                )

            # Record this request
            self.ip_requests[ip].append(now)

        # Continue processing request
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper to extract client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

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
