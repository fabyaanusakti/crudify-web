from django import template

register = template.Library()

@register.filter
def get_editor_name(user):
    if not user:
        return ""
    return user.get_full_name() or user.username