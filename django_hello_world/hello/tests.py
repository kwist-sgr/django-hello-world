"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from django_hello_world.hello.models import StoredHttpRequest

from models import Profile, StoredHttpRequest


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello!')


class ProfileTest(TestCase):

    def test_profile(self):
        user = User.objects.get(id=1)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        keywords = ('Name', 'Last name', 'Date of birth', 'Bio', 'Email',
                    'Jabber', 'Skype', 'Other contacts')
        for keyword in keywords:
            self.assertContains(response, keyword)

        profile = Profile.objects.get(user=user)
        values = [
            user.first_name, user.last_name, user.email, profile.birthday.isoformat(),
            profile.bio.replace('\n', '<br />'), profile.contacts.replace('\n', '<br />'),
            profile.jabber, profile.skype
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
