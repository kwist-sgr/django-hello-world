"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os
import subprocess

from random import randint, choice
from datetime import date
from StringIO import StringIO

from django.contrib.auth.models import User
from django.conf import settings as conf

from django.template import Template, Context
from django.core.management import call_command

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client, RequestFactory

from django_hello_world.hello.models import Profile, StoredHttpRequest, \
    ModelAction
from django_hello_world.hello.forms import ProfileEditForm
from django_hello_world.hello.views import ProfileEditView
from django_hello_world.hello.testing import UserFactory, ProfileFactory, \
    StoredHttpRequestFactory, ModelActionFactory


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello!')


class ProfileTest(TestCase):

    def test_profile(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        keywords = ('Name', 'Last name', 'Date of birth', 'Bio', 'Email',
                    'Jabber', 'Skype', 'Other contacts')
        for keyword in keywords:
            self.assertContains(response, keyword)

        profile = Profile.objects.get(user__id=1)
        values = [
            profile.first_name,
            profile.last_name,
            profile.email,
            profile.birthday.isoformat(),
            profile.bio.replace('\n', '<br />'),
            profile.contacts.replace('\n', '<br />'),
            profile.jabber,
            profile.skype
        ]
        for value in values:
            self.assertContains(response, value)


class StoreHttpRequestTest(TestCase):

    def test_store(self):
        url = '/music/bands/the_beatles?sort=name'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

        store = list(StoredHttpRequest.objects.all())
        self.assertTrue(store)
        self.assertEqual(len(store), 1)

        item = store[0]
        self.assertTrue(item.date)
        self.assertTrue(item.remote_addr)
        self.assertFalse(item.user)
        self.assertFalse(item.is_secure)
        self.assertFalse(item.referer)
        self.assertFalse(item.user_agent)

        self.assertEqual(item.method, 'GET')
        self.assertEqual(item.full_path, url)

    def test_store_headers(self):
        url = '/music/bands/the_beatles?sort=name'
        headers = {
            'HTTP_USER_AGENT': 'Chrome',
            'HTTP_REFERER': '/music/search',
            'REMOTE_ADDR': '10.1.1.1.'
        }
        response = self.client.get(url, **headers)
        self.assertEqual(response.status_code, 404)

        store = list(StoredHttpRequest.objects.all())
        self.assertTrue(store)
        self.assertEqual(len(store), 1)

        item = store[0]
        self.assertTrue(item.date)
        self.assertFalse(item.user)
        self.assertFalse(item.is_secure)

        self.assertEqual(item.remote_addr, headers['REMOTE_ADDR'])
        self.assertEqual(item.referer, headers['HTTP_REFERER'])
        self.assertEqual(item.user_agent, headers['HTTP_USER_AGENT'])
        self.assertEqual(item.method, 'GET')
        self.assertEqual(item.full_path, url)

    def test_main_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'requests')

    def test_first_10_http_request(self):
        count = 15
        for j in xrange(1, count + 1):
            self.client.get('/test_url/%d/' % j)

        response = self.client.get('/requests')
        self.assertEqual(response.status_code, 200)

        keywords = ('DateTime', 'User', 'Method', 'User-Agent',
                    'Full path', 'GET')
        for keyword in keywords:
            self.assertContains(response, keyword)

        for j in xrange(1, 11):
            self.assertContains(response, '/test_url/%d/' % j)
        for j in xrange(11, 20):
            self.assertNotContains(response, '/test_url/%d/' % j)


class SettingsProcessorTest(TestCase):

    def test_processor(self):
        response = self.client.get('/')
        self.assertTrue('settings' in response.context)
        self.assertEqual(response.context['settings'], conf)


class ProfileEditTest(TestCase):

    def test_anonymous_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Login')
        self.assertNotContains(response, 'Edit')
        self.assertNotContains(response, 'Logout')
        self.assertNotContains(response, '(Admin)')

    def test_authenticated(self):
        user = User.objects.get(id=1)
        self.assertTrue(self.client.login(username=user.username, password='admin'))

        response = self.client.get('/')
        self.assertNotContains(response, 'Login')
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Logout')
        self.assertContains(response, '(%s)' % user.username)
        url = reverse('admin:%s_%s_change' % (user._meta.app_label, user._meta.module_name), args=[user.id])
        self.assertContains(response, url)

    def test_auth_edit(self):
        id = 1
        url = '/profile/%d/edit/' % id
        response = self.client.get(url)
        self.assertRedirects(response, '%s?next=%s' % (conf.LOGIN_URL, url))

        profile = Profile.objects.get(user__id=id)
        self.assertTrue(self.client.login(username=profile.user.username, password='admin'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')

        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], ProfileEditForm))
        self.assertTrue('view' in response.context)
        self.assertTrue(isinstance(response.context['view'], ProfileEditView))
        self.assertTrue('object' in response.context)
        self.assertTrue('profile' in response.context)
        self.assertEqual(response.context['object'], response.context['profile'])
        self.assertTrue(isinstance(response.context['object'], Profile))

        # Check Submit
        self.assertTrue('csrf_token' in response.context)
        data = {
            'csrfmiddlewaretoken': response.context['csrf_token'],
            'first_name': 'new name',
            'last_name': 'new last name',
            'jabber': 'yandex',
            'birthday': '2012-01-10',
            'skype': 'ejvdyrtrgdgfg',
            'photo': '',
            'contacts': 'wer\ntyiuy\nchf',
            'bio': 'arhhdhjrgrd\njertueut\n\nrjhtuertu',
        }

        r = self.client.post(url, data=data)
        self.assertRedirects(r, '/')

        profile = Profile.objects.get(user__id=id)
        for key, value in data.iteritems():
            if key != 'csrfmiddlewaretoken':
                if key == 'birthday':
                    self.assertEqual(value, getattr(profile, key).strftime('%Y-%m-%d'))
                else:
                    self.assertEqual(value, getattr(profile, key))

        # Check error
        data['birthday'] = 'dfhgh'
        r = self.client.post(url, data=data)
        self.assertContains(response, 'ul class="errorlist"')

    def test_ajax_submit(self):
        id = 1
        url = '/profile/%d/edit/' % id
        profile = Profile.objects.get(user__id=id)

        self.assertTrue(self.client.login(username=profile.user.username, password='admin'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Edit Profile')

        self.assertTrue('form' in response.context)
        self.assertTrue(isinstance(response.context['form'], ProfileEditForm))
        self.assertTrue('view' in response.context)
        self.assertTrue(isinstance(response.context['view'], ProfileEditView))
        self.assertTrue('object' in response.context)
        self.assertTrue('profile' in response.context)
        self.assertEqual(response.context['object'], response.context['profile'])
        self.assertTrue(isinstance(response.context['object'], Profile))

        # Check Ajax Submit
        self.assertTrue('csrf_token' in response.context)
        data = {
            'csrfmiddlewaretoken': response.context['csrf_token'],
            'first_name': 'new name',
            'last_name': 'new last name',
            'jabber': 'yandex',
            'birthday': '2012-01-10',
            'skype': 'ejvdyrtrgdgfg',
            'photo': '',
            'contacts': 'wer\ntyiuy\nchf',
            'bio': 'arhhdhjrgrd\njertueut\n\nrjhtuertu',
        }

        r = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.content, '{}')

        profile = Profile.objects.get(user__id=id)
        for key, value in data.iteritems():
            if key != 'csrfmiddlewaretoken':
                if key == 'birthday':
                    self.assertEqual(value, getattr(profile, key).strftime('%Y-%m-%d'))
                else:
                    self.assertEqual(value, getattr(profile, key))

        # Check error
        data['birthday'] = 'dfhgh'
        r = self.client.post(url, data=data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertContains(r, 'birthday')


class EditLinkTest(TestCase):

    def test_tag(self):
        html = '''
            {% load edit_link %}
            {% autoescape on %}
                {% edit_link request.user %}
            {% endautoescape %}
        '''
        template = Template(html)

        user = User.objects.get(id=1)
        request = RequestFactory().get('/')
        request.user = user
        context = Context({'request': request})

        url = reverse('admin:%s_%s_change' % (user._meta.app_label, user._meta.module_name), args=[user.id])
        self.assertTrue(url in template._render(context))


class PrintAllModelsTest(TestCase):

    def test_command(self):
        std_out = StringIO()
        std_err = StringIO()
        call_command('print_all_models', stderr=std_err, stdout=std_out)
        for str_out, str_err in zip(std_out.readlines(), std_err.readlines()):
            self.assertEquals(str_err, 'error: %s' % str_out)

    def test_bash(self):
        popen = subprocess.Popen(
            ['bash', 'print_all_models.sh'],
            stdout=subprocess.PIPE
        )
        std_out, _ = popen.communicate()
        file_path = '%s.dat' % date.today().strftime('%Y-%m-%d')
        self.assertTrue(os.path.exists(file_path))
        handle = open(file_path, 'r')
        for str_out, str_err in zip(std_out.split('\n'), handle.readlines()):
            self.assertEquals(str_err.rstrip('\n'), 'error: %s' % str_out)
        handle.close()
        os.unlink(file_path)


class SignalTest(TestCase):

    def test_ignore_model_action(self):
        for _ in xrange(randint(2, 10)):
            ModelActionFactory()

        self.assertFalse(
            ModelAction.objects.filter(model='ModelAction').count()
        )

    def test_action(self):
        types = {
            'user': lambda: UserFactory(),
            'profile': lambda: ProfileFactory(),
            'http': lambda: StoredHttpRequestFactory(user=None),
            'http_auth': lambda: StoredHttpRequestFactory()
        }

        for id, proc in types.iteritems():
            for _ in xrange(randint(2, 10)):
                proc()

        # Create
        for model in (User, Profile, StoredHttpRequest):
            self.assertEqual(
                ModelAction.objects.filter(
                    model=model.__name__,
                    action=ModelAction.ACTION_CREATE
                ).count(),
                model.objects.count()
            )

        # Modify
        modify = dict(
            (m, randint(2, m.objects.count()))
            for m in (User, Profile, StoredHttpRequest)
        )

        for model, count in modify.iteritems():
            all = list(model.objects.all())
            for obj in all[:count]:
                obj.save()

            self.assertEqual(
                ModelAction.objects.filter(
                    model=model.__name__,
                    action=ModelAction.ACTION_MODIFY
                ).count(),
                count
            )

        # Delete
        delete = dict(
            (m, randint(2, m.objects.count()))
            for m in (Profile, StoredHttpRequest)
        )

        for model, count in delete.iteritems():
            all = list(model.objects.all())
            for obj in all[:count]:
                obj.delete()

            self.assertEqual(
                ModelAction.objects.filter(
                    model=model.__name__,
                    action=ModelAction.ACTION_DELETE
                ).count(),
                count
            )
