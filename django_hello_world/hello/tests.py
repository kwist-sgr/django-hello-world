"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

from models import Profile


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class HttpTest(TestCase):
    def test_home(self):
        c = Client()
        response = c.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hello!')


class ProfileTest(TestCase):

    def test_profile(self):
        user = User.objects.get(id=1)
        response = self.client.get('profile/%d' % user.id)
        self.assertEqual(response.status_code, 200)
        keywords = ('Name', 'Last name', 'Date of birth', 'Bio', 'Email', 'Jabber', 'Skype', 'Other contacts')
        for keyword in keywords:
            self.assertContains(response, keyword)

        profile = Profile.objects.get(user=user)
        values = [user.first_name, user.last_name, user.email, profile.birthday.isoformat(),
            profile.bio, profile.contacts, profile.jabber, profile.skype]
        for value in values:
            self.assertContains(response, keyword)


