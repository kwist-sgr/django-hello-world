from django.conf import settings as conf


def django_settings_processor(request):
    return {'settings': conf}
