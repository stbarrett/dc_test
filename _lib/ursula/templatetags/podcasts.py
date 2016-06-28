from django import template
from django.template import Library, Node, TemplateSyntaxError 
register = template.Library()
                            
@register.filter(name='podcast_image')
def podcast_image(obj):
    return obj.podcast_image()