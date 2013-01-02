import re

from django import template


register = template.Library()


@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.filter
def fraction_only(decimal):
    if decimal:
        return unicode(decimal).replace('0.', '.')
    return decimal
