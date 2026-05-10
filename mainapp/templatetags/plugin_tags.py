# myapp/templatetags/plugin_tags.py

from django import template
from mainapp.models import Plugin  # Import your Plugin model

register = template.Library()

@register.simple_tag
def get_last_plugin():
    return Plugin.objects.last()
