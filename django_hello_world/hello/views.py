from annoying.decorators import render_to
from django.contrib.auth.models import User
from django_hello_world.hello.models import Profile


@render_to('hello/home.html')
def home(request):
    users = User.objects.filter()
    return {'users': users}


@render_to('hello/profile.html')
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    values = {
        'name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'birthday': None,
        'bio': None,
        'contacts': None,
        'jabber': None,
        'skype': None
    }
    profile = Profile.objects.get_or_None(user=user)
    if profile:
        values.update(
            bio=profile.bio,
            birthday=profile.birthday,
            contacts=profile.contacts,
            jabber=profile.jabber,
            skype=profile.skype
        )
    return {'values': values}