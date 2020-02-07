from django.core.cache import cache

from protector import consts


class UserAgentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            cache_key = f"user_{request.user.id}"
            cache.set(cache_key, request.META.get("HTTP_USER_AGENT"),
                      timeout=consts.USER_AGENT_LIFETIME)
        response = self.get_response(request)
        return response
