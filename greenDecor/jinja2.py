# @Author: Javed Ahamad
# @Date:   2017-02-12
# @Email:  javedahamad4@gmail.com
# @Filename: jinja2.py



from __future__ import absolute_import  # Python 2 only
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment
from django.contrib import messages


def get_no_of_cart_items(request):
    """
    return no of cart items
    """
    from web.views import getAllContext
    from core.models import CartItem
    try:
        context = getAllContext(request)
        cart_items = CartItem.objects.filter(cart=context['cart']).count()
        return cart_items
    except Exception as e:
        return 0


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
        'messages': messages.get_messages,
        'get_no_of_cart_items': get_no_of_cart_items
    })
    return env
