from django import template
from django.core.urlresolvers import reverse
#from django.utils.encoding import iri_to_uri
#from django.utils.safestring import mark_safe
from django.utils.html import format_html


register = template.Library()


@register.tag(name='edit_link')
def get_edit_link(parser, token):
    #parser.delete_first_token()
    tokens = token.contents.split()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError("'%r' tag requires at least 1 arguments." % tokens[0])
    return EditLinkNode(tokens[1])

get_edit_link.is_safe = True


class EditLinkNode(template.Node):

    def __init__(self, user):
        self.user = template.Variable(user)

    def render(self, context):
        try:
            object = self.user.resolve(context)
        except template.VariableDoesNotExist:
            return ''
        url = reverse('admin:%s_%s_change' % (object._meta.app_label, object._meta.module_name), args=[object.id])
        r = u'<a href="%s">(%s)</a>' % (url, object.__unicode__())
        return r
