from django import template # to handle templates variables and context
from django.db import connection, transaction
from ursula.models import Tag, Tag_List


# register our template tags to be able to use them in our templates
register = template.Library() 


## Create Node
class TagsNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):
        context[self.varname] = Tag.objects.all().filter(is_active = 1).order_by('name')
        return ''
#parser
def do_list_tags(parser, token):
    tokens = token.contents.split()
    return TagsNode(tokens[2])
register.tag('list_tags', do_list_tags)


class TagsForTypeNode(template.Node):
    def __init__(self, type_id, varname):
        self.varname = varname
        self.type_id = type_id 
        
    def render(self, context):
        type_id = int(template.resolve_variable(self.type_id, context))
        context[self.varname] = Tag_List.objects.values('tag__name', 'tag__slug', 'tag__id').distinct().filter(item__type = type_id, is_active = 1).order_by('tag__slug')
        return ''
#parser
def do_list_tags_for_type(parser, token):
    tokens = token.contents.split()
    return TagsForTypeNode(tokens[1], tokens[3])
register.tag('list_tags_for_type', do_list_tags_for_type)