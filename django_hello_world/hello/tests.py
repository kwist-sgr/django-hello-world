"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User
from django.conf import settings as conf

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from django_hello_world.hello.models import Profile, StoredHttpRequest
from django_hello_world.hello.forms import ProfileEditForm
from django_hello_world.hello.views import ProfileEditView


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

    def test_authenticated(self):
        user = User.objects.get(id=1)
        self.assertTrue(self.client.login(username=user.username, password='admin'))

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Login')
        self.assertContains(response, 'Edit')
        self.assertContains(response, 'Logout')

    def test_auth_edit(self):
        id = 1
        url = '/profile/%d/edit/' % id
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('location' in response)
        self.assertTrue(conf.LOGIN_URL in response['location'])
        self.assertTrue('next=%s' % url in response['location'])

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
