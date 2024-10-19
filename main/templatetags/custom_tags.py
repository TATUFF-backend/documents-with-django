import os
from django import template

register = template.Library()

@register.filter
def filename(value):
    """Fayl yo‘lidan faqat fayl nomini qaytaradi."""
    if value:
        file_name = os.path.basename(value.name)
        return file_name if (len(file_name) < 40) else f"{file_name[:20]}...{file_name[-10:]}"
    return ''
