from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import Http404
import json
from django.conf import settings
from django.contrib.auth.models import User
from core.models import *
from django.db.models import Q
from greenDecor.settings import *
from django.core.mail import EmailMessage
import urllib2
import os
import requests

def authenticate_user(username, password):
    """
    Util function for logging in user
    """
    current_user = authenticate(username=username, password=password)
    authed = False
    if current_user:
        authed = True
    return authed, current_user

def registerUser(*args,**kwargs):
    """function to register the user"""
    email=kwargs.pop("email")
    password=kwargs.pop("password")
    # mobile=kwargs.pop("mobile")
    username = kwargs.pop("username")
    # usertype = kwargs.pop("usertype")
    user=User.objects.create_user(username,email,password)
    # UserProfile.objects.create(user=user,userType=usertype,mobile=username)
    return user

def add_plant_quantity(request,plant_id,quantity):
    """
    Function for add plant stock quantity
    """
    plant = Plants.objects.get(id=plant_id)
    if PlantStock.objects.filter(plant = plant,user=request.user).exists():
        ps = PlantStock.objects.get(plant = plant,user=request.user)
        ps.quantity = quantity
        ps.save()
        return True, 'quantity updated successfully'
    else:
        PlantStock.objects.create(plant = plant,user=request.user,quantity=quantity)
        return True, 'quantity added successfully'
def delete_plant_stock(request,ps_id):
    """
    Function for deleting plant stock
    """
    try:
        ps = PlantStock.objects.get(id=ps_id)
        ps.delete()
    except:
        return False
    return True

from django.http import HttpResponse
import cStringIO as StringIO
from xhtml2pdf import pisa
from html5lib import treebuilders, inputstream
from django.template.loader import get_template
from django.template import Context
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = context_dict
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def send_message(*args,**kwargs):
    """
    Function for sending message and otp
    """
    try:
        mobiles=kwargs.pop("mobiles")
        message = kwargs.pop("message")
        url = 'https://www.proactivesms.in/sendsms.jsp?user={user}&password={password}&senderid={sender_id}&mobiles={mobiles}&sms={message}'.format(
            user = os.environ.get('SMS_USER'),
            password = os.environ.get('SMS_PASSWORD'),
            sender_id = os.environ.get('SMS_SENDER_ID'),
            mobiles = mobiles,
            message = message
        )
        result_data = requests.get(url)
        return result_data.content
    except Exception as e:
        return str(e)


def send_email(*args,
**kwargs):
    """
    function for sending mail
    """
    subject = kwargs.pop("subject")
    msg_body = kwargs.pop("msg_body")
    emails = kwargs.pop("emails")
    msg = EmailMessage(subject, msg_body, DEFAULT_FROM_EMAIL, [emails])
    msg.content_subtype = "html"
    msg.send()
    return True

def trigger_mail(s,bk):
    if s=='delivered':
        text = '<p>Thank you for shopping with Green Decor . Your order id '+str(bk.id)+' has been delivered. We hope you enjoyed the business experience with us . Hope to serve you soon. Have a healthy and green life.  </p>'
        html_content = get_template('email_templates/change-status.html.j2').render({'booking': bk,'title':'Order Delivered','text':text})
        send_email(subject='Order Delivered',msg_body=html_content,emails=bk.user.email)
        m = 'Thank you for shopping with Green Decor . Your order id '+str(bk.id)+' has been delivered.'
        send_message(mobiles=bk.shipping_phone,message=m)
    elif s=='dispatched':
        text = '<p>Your order no. '+str(bk.id)+' is out for delivery Please be ready to receive it. Your total bill is Rs. '+str(bk.amount)+'</p>'
        html_content = get_template('email_templates/change-status.html.j2').render({'booking': bk,'title':'Order Dispatched','text':text})
        send_email(subject='Order Dispatched',msg_body=html_content,emails=bk.user.email)
        m = 'Dear Customer\
        Your order no.  '+str(bk.id)+' is out for delivery Please be ready to receive it. Your total bill is Rs. '+str(bk.amount)+'\
        Thanks'
        send_message(mobiles=bk.shipping_phone,message=m)
    elif s=='canceled':
        text = '<p>Thank you for showing interest in our products. But we regret to inform that we would not be able to fulfil your order at this time. We would surely get back to you once we are ready to complete your transaction.</p><p>Thank you and have a green day.</p>'
        html_content = get_template('email_templates/change-status.html.j2').render({'booking': bk,'title':'Order Canceled','text':text})
        send_email(subject='Order Canceled',msg_body=html_content,emails=bk.user.email)
        m = 'Thank you for showing interest in our products. But we regret to inform that we would not be able to fulfil your order id '+bk.id+' at this time. We would surely get back to you once we are ready to complete your transaction.'
        send_message(mobiles=bk.shipping_phone,message=m)
    else:
        text = '<p> The status of your Order No.'+str(bk.id)+' has been changed to '+bk.status+'</p>'
        html_content = get_template('email_templates/change-status.html.j2').render({'booking': bk,'title':'Order Status Changed','text':text})
        send_email(subject='Order Status Changed',msg_body=html_content,emails=bk.user.email)
        m = 'your order id '+str(bk.id)+' is'+str(bk.status)+''
        send_message(mobiles=bk.shipping_phone,message=m)

def get_category_page_plants(category=None, page=1, num=8):
    """
    return category plants with pagination
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    if category is None:
        return []
    plants = Plants.objects.filter(Q(category=category) | Q(category=category.parent_category),active=True).order_by('-id')
    paginator = Paginator(plants, num)
    try:
        plant = paginator.page(page)
    except PageNotAnInteger:
        plant = paginator.page(1)
    except EmptyPage:
        plant = paginator.page(paginator.num_pages)
    return plant




def get_category_page_gifting(category=None, page=1, num=8):
    """
    return category plants with pagination
    """
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    if category is None:
        return []
    plants = GiftingCategory.objects.filter(Q(category=category) | Q(category=category.parent_category),active=True).order_by('-id')
    paginator = Paginator(plants, num)
    try:
        plant = paginator.page(page)
    except PageNotAnInteger:
        plant = paginator.page(1)
    except EmptyPage:
        plant = paginator.page(paginator.num_pages)
    return plant
