from django import template

register = template.Library()

@register.filter(name="split")
def split(value, arg):
    split_list = value.split(arg)
    return split_list[:-1]
