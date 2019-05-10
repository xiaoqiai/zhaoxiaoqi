from django import template
from app1.models import xiala

register = template.Library()

@register.simple_tag
def get_categories():
    return xiala.objects.all()