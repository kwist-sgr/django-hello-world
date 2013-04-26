#from django.forms import ModelForm
from django.forms import ModelForm
#from django.http import HttpResponseForbidden

from django_hello_world.hello.models import Profile


class ProfileEditForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ('user')
