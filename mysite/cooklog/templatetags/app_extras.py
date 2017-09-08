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


@register.simple_tag
def include_anything(file_name):
    return open(file_name).read()

@register.simple_tag
def include_dish_diagram(dish_id):
    import os.path
    # file_name = "mysite/media/dish_flow_svg/dish_flow_"+str(dish_id)+".svg"
    # file_name = "/Users/katiequinn/Documents/cooklog/mysite/media/dish_flow_svg/dish_flow_"+str(dish_id)+".svg"
    file_name = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                             "media/dish_flow_svg/dish_flow_"+str(dish_id)+".svg")
    if os.path.exists(file_name):
        return open(file_name).read()
    else:
        return " "
