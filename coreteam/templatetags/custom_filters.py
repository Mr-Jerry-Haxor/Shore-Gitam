from django import template

register = template.Library()


@register.filter(name="format_text")
def format_text(value):
    # Replace underscores with spaces and capitalize each word
    return value.replace("_", " ").title()
