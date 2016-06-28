from django import template
from django.template import Library, Node, TemplateSyntaxError 
register = template.Library()
from ursula.models import Type


class TypesNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):
        context[self.varname] = Type.objects.all().order_by('name')
        return ''

def do_list_types(parser, token): 
    tokens = token.contents.split()
    return TypesNode(tokens[2])

register.tag('list_types', do_list_types)