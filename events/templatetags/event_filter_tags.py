from django import template

register = template.Library()


@register.filter(name="split")
def split(value, arg):
    values_list = value.split(arg)
    return values_list[:-1]
