from random import choice, randint
from string import ascii_lowercase, digits

import factory

from django.contrib.auth.models import User
from django_hello_world.hello.models import Profile, StoredHttpRequest, \
    ModelAction


FIRST_NAME_LIST = ['Daniel', 'Jose', 'Robert', 'Miguel']
LAST_NAME_LIST = ['Moore', 'Harris', 'Obama', 'Lopez']
TEST_PASSWORD = 'test123456'
random_string = lambda n: ''.join(choice(ascii_lowercase + digits) for _ in xrange(n))


class UserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    first_name = factory.Sequence(lambda n: choice(FIRST_NAME_LIST))
    last_name = factory.Sequence(lambda n: choice(LAST_NAME_LIST))
    password = factory.PostGenerationMethodCall('set_password', TEST_PASSWORD)
    username = factory.LazyAttribute(lambda o: o.email)

    @factory.lazy_attribute_sequence
    def email(self, n):
        return '{0}.{1}.{2}@gmail.com'.format(self.first_name, self.last_name, n).lower()


class ProfileFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Profile

    user = factory.SubFactory(UserFactory)


class StoredHttpRequestFactory(factory.DjangoModelFactory):
    FACTORY_FOR = StoredHttpRequest

    user = factory.SubFactory(UserFactory)
    method = factory.LazyAttribute(lambda o: choice(['GET', 'POST', 'HEAD']))
    full_path = factory.LazyAttribute(lambda o: '/detail/%s' % random_string(7))
    user_agent = factory.LazyAttribute(
        lambda o: 'Mozilla/5.0 (compatible; %s)' % random_string(10).upper()
    )
    referer = factory.LazyAttribute(lambda o: '/view/%s' % random_string(7))
    remote_addr = factory.LazyAttribute(
        lambda o: '%s.%s.%s.%s' % (randint(1, 255), randint(1, 255), randint(1, 255), randint(1, 255))
    )


class ModelActionFactory(factory.DjangoModelFactory):
    FACTORY_FOR = ModelAction

    pk = factory.Sequence(lambda n: n)
    app_label = factory.Iterator(['profile', 'user', 'group'])
    model = factory.Iterator(['Profile', 'User', 'Group'])
    action = factory.LazyAttribute(
        lambda o: choice([ModelAction.ACTION_CREATE, ModelAction.ACTION_MODIFY, ModelAction.ACTION_DELETE])
    )
