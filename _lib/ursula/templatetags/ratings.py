from django import template
register = template.Library()
                            
@register.filter(name='average_rating')
def average_rating(obj):
    return obj.get_average_rating()