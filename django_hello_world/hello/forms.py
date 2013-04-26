from django.forms import ModelForm, DateField, widgets

from django_hello_world.hello.models import Profile


class CalendarWidget(widgets.TextInput):

    class Media:
        css = {'all': "/css/jquery-ui.css"}
        js = ("/js/jquery-ui.js")


class ProfileEditForm(ModelForm):

    #birthday = DateField(widget=CalendarWidget)

    class Meta:
        model = Profile
        exclude = ('user')
