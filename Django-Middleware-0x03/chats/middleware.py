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
