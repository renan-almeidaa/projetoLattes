from datetime import datetime
from django import template

register = template.Library()

@register.simple_tag
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        f_querystring = filter(lambda p: p.split('=')[0]!=field_name, querystring)
        e_querystring = '&'.join(f_querystring)
        url='{}&{}'.format(url, e_querystring)

    return url

@register.filter
def replace(value, arg):
    """
    Replacing filter
    Use `{{ "aaa"|replace:"a|b" }}`
    """
    if len(arg.split('|')) != 2:
        return value

    what, to = arg.split('|')
    return value.replace(what, to)


@register.filter
def convert_str_date(value):
    if(len(value)>0):
        dia = value[0:2]
        mes = value[2:4]
        ano = value[4:len(value)]
        value = dia + "/" + mes + "/" + ano
    else: value = "Não informado"

    return value