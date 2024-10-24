
from django import template
#this allow us to register the multiply tage 
register = template.Library()


@register.filter(name='multiply')
def multiply(a,b):
    return a*b


