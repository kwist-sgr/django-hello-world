from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Print all project models and the count of objects in every model'

    def handle(self, *args, **options):
        try:
            def get_model_info(cls):
                obj = cls.model_class()
                return '[%(module)s] %(app_label)s, %(model)s, %(count)d' % {
                    'module': obj.__module__,
                    'app_label': cls.name,
                    'model': obj.__name__,
                    'count': obj.objects.count()
                }

            data = list(ContentType.objects.all())
            output = [get_model_info(j) for j in data]
            self.stdout.write('\n'.join(output))
            self.stderr.write('\n'.join(map(lambda s: 'error: %s' % s, output)))
        except Exception, e:
            raise CommandError(e)
