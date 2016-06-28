from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.contrib.auth import REDIRECT_FIELD_NAME

from facebook.djangofb import get_facebook_client
from facebookconnect.models import FacebookTemplate, FacebookProfile

register = template.Library()

#def is_facebook_logged_in():
    
#    if isinstance(user, FacebookProfile):
#        p = user
#    else:
#        p = user.facebook_profile
        
#    return "test"

#@register.filter(name='is_facebook_logged_in')


## Create Node
class IsFacebookLoggedIn(template.Node):
    def __init__(self, user):
        self.user = user
        
    def render(self, context):
        
        return request.user.id

#parser
def is_facebook_logged_in(parser, token):
  tokens = token.split_contents();
  return IsFacebookLoggedIn(tokens[1])

register.tag('is_facebook_logged_in', is_facebook_logged_in)