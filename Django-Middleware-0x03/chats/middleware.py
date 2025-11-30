import logging
from datetime import datetime

# Configure logger to write to a file
logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")  # file will be created in project root
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# class RequestLoggingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         user = request.user if request.user.is_authenticated else "Anonymous"
#         log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
#         logger.info(log_message)

#         response = self.get_response(request)
#         return response

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine user identity
        user = request.user if request.user.is_authenticated else "Anonymous"

        # Log the required information
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Continue processing the request
        response = self.get_response(request)
        return response
        
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Current server time (24-hour format)
        current_hour = datetime.now().hour

        # Allowed window: between 6AM (06:00) and 9PM (21:00)
        if current_hour < 6 or current_hour >= 21:
            return HttpResponseForbidden("Access to chat is restricted outside 6AM–9PM.")

        # Continue normal request processing
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Dictionary to track requests per IP
        # Format: { ip: [timestamps] }
        self.ip_requests = defaultdict(list)
        self.limit = 5          # max messages
        self.window = 60        # seconds (1 minute)

    def __call__(self, request):
        # Only enforce on POST requests (chat messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = time.time()

            # Clean up old timestamps outside the window
            self.ip_requests[ip] = [
                ts for ts in self.ip_requests[ip] if now - ts < self.window
            ]

            # Check if limit exceeded
            if len(self.ip_requests[ip]) >= self.limit:
                return HttpResponseForbidden(
                    "Message limit exceeded: max 5 per minute."
                )
            # Record this request timestamp
            self.ip_requests[ip].append(now)

        # Continue normal processing
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Helper to extract client IP address."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "")
