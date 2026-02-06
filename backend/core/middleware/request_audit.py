import logging
import time

logger = logging.getLogger(__name__)


class RequestAuditMiddleware:
    """
    Middleware to:
    1. Log request metadata and execution time
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)

        # ---- LOGGING (RESPONSE PHASE) ----
        duration_ms = (time.time() - start_time) * 1000

        user = request.user if request.user.is_authenticated else "anonymous"
        ip = self.get_client_ip(request)

        logger.info(
            "%s %s %s [%s] %s %.2fms",
            request.method,
            request.path,
            response.status_code,
            user,
            ip,
            duration_ms,
        )

        return response

    def get_client_ip(self, request):
        """
        Get client IP address from request headers if behind a proxy, otherwise from remote address.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
