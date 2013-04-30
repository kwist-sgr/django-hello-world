from django.views.generic.edit import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from annoying.decorators import render_to, ajax_request

from django_hello_world.hello.models import Profile, StoredHttpRequest
from django_hello_world.hello.forms import ProfileEditForm


@render_to('hello/home.html')
def home(request):
    return {'profile': Profile.objects.select_related('user').get(user__id=1)}


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

    @ajax_request
    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            self.object = self.get_object()
            form = self.get_form(self.get_form_class())
            if form.is_valid():
                self.object = form.save()
                return {}
            else:
                return form.errors
        else:
            return super(ProfileEditView, self).post(requests, *args, **kwargs)

    def get_queryset(self):
        return super(ProfileEditView, self).get_queryset().select_related('user')
