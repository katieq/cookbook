import re
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

def create_hashtag_link(tag):
    url = "/cooklog/search/?q={}".format(tag)
    # or: url = reverse("hashtag", args=(tag,))
    return '<a href="{}">{}</a>'.format(url, tag)


@register.filter(name='hashtag_links')
def hashtag_links(value):
    return mark_safe(
                     re.sub(r"#(\w+)", lambda m: create_hashtag_link(m.group(1)),
                            conditional_escape(value)))
