from annoying.decorators import render_to
from django.contrib.auth.models import User
from django_hello_world.hello.models import Profile, StoredHttpRequest


@render_to('hello/home.html')
def home(request):
    users = User.objects.filter()
    try:
        profile = Profile.objects.select_related().get(user__id=1)
        profile_values = {
            'name': profile.user.first_name,
            'last_name': profile.user.last_name,
            'email': profile.user.email,
            'bio': profile.bio,
            'birthday': profile.birthday,
            'contacts': profile.contacts,
            'jabber': profile.jabber,
            'skype': profile.skype
        }
    except:
        profile_values= {}
    return {'users': users, 'profile': profile_values}


@render_to('hello/requests.html')
def requests(request):
    first10 = StoredHttpRequest.objects.order_by('date')[:10]
    return {'first10': first10}
