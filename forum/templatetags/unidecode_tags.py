from django import template
from django.template.defaultfilters import stringfilter
from unidecode import unidecode

register = template.Library()

@register.filter(name='unidecode')
@stringfilter
def unidecode_filter(value):
    return unidecode(value)