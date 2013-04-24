from annoying.decorators import render_to
from django.contrib.auth.models import User
from django_hello_world.hello.models import Profile, StoredHttpRequest


@render_to('hello/home.html')
def home(request):
    users = User.objects.filter()
    try:
        profile = Profile.objects.get(user__id=1)
        profile_values = {
            'name': profile.first_name,
            'last_name': profile.last_name,
            'email': profile.email,
            'bio': profile.bio,
            'birthday': profile.birthday,
            'contacts': profile.contacts,
            'jabber': profile.jabber,
            'skype': profile.skype
        }
    except:
        profile_values = {}
    return {'users': users, 'profile': profile_values}


@render_to('hello/requests.html')
def requests(request):
    first10 = StoredHttpRequest.objects.order_by('id')[:10]
    return {'first10': first10}
