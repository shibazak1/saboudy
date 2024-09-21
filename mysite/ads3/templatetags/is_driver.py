from ads3.models import Driver
from django import template
#this allow us to register the multiply tage 
register = template.Library()


@register.filter(name='is_driver')
def is_driver(user):
    return isinstance(user,Driver)

