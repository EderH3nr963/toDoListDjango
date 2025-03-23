from django import template

register = template.Library()

@register.filter(name='div')
def div(value, arg):
    """
    Divide o valor pelo argumento
    """
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

@register.filter(name='mul')
def mul(value, arg):
    """
    Multiplica o valor pelo argumento
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0 