from django import template # to handle templates variables and context
from ursula.models import Person, Person_List


# register our template tags to be able to use them in our templates
register = template.Library() 


## Create Node
class PeopleNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):
        context[self.varname] = Person.objects.all().filter(is_active = 1).order_by('first_name')
        return ''

#parser
def do_list_People(parser, token):
    tokens = token.contents.split()
    return PeopleNode(tokens[2])


register.tag('list_people', do_list_People)
