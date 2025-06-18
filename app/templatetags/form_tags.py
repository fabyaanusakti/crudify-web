from django import template

register = template.Library()

@register.filter(name='add_error_class')
def add_error_class(field, errors):
    classes = field.field.widget.attrs.get('class', '')
    if errors:
        classes += ' is-invalid'
    return field.as_widget(attrs={'class': classes})