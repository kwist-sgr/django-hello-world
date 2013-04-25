from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from annoying.decorators import render_to
from django.contrib.auth.models import User

from django_hello_world.hello.models import Profile, StoredHttpRequest
from django_hello_world.hello.forms import ProfileEditForm


@render_to('hello/home.html')
def home(request):
    return {'profile': Profile.objects.get(user__id=1)}


@render_to('hello/requests.html')
def requests(request):
    first10 = StoredHttpRequest.objects.order_by('id')[:10]
    return {'first10': first10}


class ProfileEditView(UpdateView):

    model = Profile
    template_name = 'hello/profile_edit.html'
    form_class = ProfileEditForm
    success_url = '/'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #if int(kwargs['pk']) != request.user.id:
        #    return HttpResponseForbidden()
        return super(ProfileEditView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        return super(ProfileEditView, self).form_valid(form)

    def get_queryset(self):
        return super(ProfileEditView, self).get_queryset().select_related('user')
