from django.forms import ModelForm, DateField, widgets

from django_hello_world.hello.models import Profile


class ProfileEditForm(ModelForm):

    class Meta:
        model = Profile
        exclude = ('user')
