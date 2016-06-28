from django import template # to handle templates variables and context
from ursula.models import Location, Location_List


# register our template tags to be able to use them in our templates
register = template.Library() 

class LocationsNode(template.Node):
    def __init__(self, varname):
        self.varname = varname
        
    def render(self, context):
        context[self.varname] = Location.objects.all().filter(is_active = 1).order_by('name')
        return ''

def do_list_locations(parser, token): 
    tokens = token.contents.split()
    return LocationsNode(tokens[2])

register.tag('list_locations', do_list_locations)
