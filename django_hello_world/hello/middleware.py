
from django_hello_world.hello.models import StoredHttpRequest


class RequestStoreMiddleware(object):

    def process_request(self, request):
        user = request.user if request.user.is_authenticated() \
            else None
        StoredHttpRequest.objects.create(
            user=user,
            method=request.method,
            is_secure=request.is_secure(),
            full_path=request.get_full_path(),
            user_agent=request.META.get('HTTP_USER_AGENT'),
            referer=request.META.get('HTTP_REFERER'),
            remote_addr=request.META['REMOTE_ADDR']
        )
