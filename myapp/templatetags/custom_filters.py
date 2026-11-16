from django import template

register = template.Library()

print("Custom filters loaded")  # Add this line for debugging

@register.filter(name='mul')
def mul(value, arg):
    return value * arg
