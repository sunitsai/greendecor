# @Author: Javed Ahamad
# @Date:   2017-02-12
# @Email:  javedahamad4@gmail.com
# @Filename: urls.py


from django.shortcuts import render
from django.views.generic import DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.http import Http404
import json
from django.core import serializers
from django.http import HttpResponse
import random
from django.conf import settings
from core.models import *
from core.utils import *
from .forms import *
from coupon.forms import *
import re
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.sessions.models import Session
from django.core import serializers
from django.db.models import Q
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, JsonResponse
from greenDecor.settings import *

# Create your views here.
def getAllContext(request):
    if 'cart_id' in request.session and  request.user.is_authenticated:
        # dlscds
        if Carts.objects.filter(user = request.user).count()==0:
            cart = Carts.objects.create(user = request.user,name=request.user.username)
            old_cart = Carts.objects.get(id = int(request.session['cart_id']))
            if CartItem.objects.filter(cart=old_cart).count() > 0:
                old_cart_item = CartItem.objects.filter(cart=old_cart)
                old_cart_item.update(cart=cart)
                old_cart.delete()
                del request.session['cart_id']
        else:
            cart = Carts.objects.get(user=request.user)
            if CartItem.objects.filter(cart=cart).count() == 0:
                old_cart = Carts.objects.get(id = int(request.session['cart_id']))
                old_cart_item = CartItem.objects.filter(cart=old_cart)
                old_cart_item.update(cart=cart)
                old_cart.delete()
                del request.session['cart_id']
    elif 'cart_id' in request.session and  not request.user.is_authenticated:
        cart = Carts.objects.get(id=int(request.session['cart_id']))

    elif request.user.is_authenticated and 'cart_id' not in request.session:
        if Carts.objects.filter(user = request.user).count()==0:
            cart = Carts.objects.create(user = request.user,name=request.user.username)
        else:
            cart = Carts.objects.get(user = request.user)
    else:
        cart = Carts.objects.create(name='Guest cart')
        cart_id = cart.id
        request.session['cart_id'] = str(cart_id)
    context = {}
    context['cartCount'] = CartItem.objects.filter(cart=cart).count()
    context['cart'] = cart
    context['categories'] = Category.objects.all()
    context['delivery_charge_config'] = DeliveryChargeConfig.objects.all()[:1]
    context['offer_slider'] = OfferSlider.objects.last()
    return context


def index(request, **kwargs):
    """
    Renders the landing page of the Greendecore
    """
    context = getAllContext(request)
    page_data = OnlineNersery.objects.first()
    context['title'] = page_data.meta_title
    context['meta_desc'] = page_data.meta_description
    context['meta_keyword'] = page_data.meta_keyword
    context['long_content'] = page_data.long_content
    context['page_data'] = page_data
    context['category_data'] = OnlineNerseryCategory.objects.all()
    return render(request, "web/online-nursery.html.j2", context)
    # comment regular landing page
    # context['title'] = 'Buy Plants Online Delhi, Best Online Plant Nursery in India | Green Decor'
    # context['meta_desc'] = 'Buy all types of garden fresh plants online in Delhi NCR at the best price at Green Decor. Green Decor is one stop online plant nursery in India to buy indoor and outdoor plants, seeds and pots online in Delhi, Gurgaon and Noida.'
    # context['meta_keyword'] = 'Plant in Delhi, buying plants in online, buy plants online Delhi, natural plants online Delhi, natural plants shopping online, buy plants online Delhi, online plant nursery Delhi, plants online Delhi, order plants online, garden plants in India, online plant nursery Delhi, garden plants in India, online shopping for natural plants, order plants online, buy any kind of plants online in Delhi NCR, Buy plants online Noida, Buy plants Gurgaon, online plants Faridabad'
    # context['plants'] = Plants.objects.filter(active=True)[:10]
    # context['testimonials'] = Testimonials.objects.all()[:10]
    # return render(request, "base.html.j2", context)

#function to register the user
class RegisterView(View):
    """view class to handle the user registration"""
    def get(self,request):
        form=RegistrationForm()
        context = getAllContext(request)
        context['form'] = form
        context['errors'] = {}
        context['title'] = 'Green Decor'
        context['meta_desc'] = 'Green Decor'
        context['meta_keyword'] = 'Green Decor'
        return render(request,"web/registration.html.j2",context)
    def post(self,request):
        form=RegistrationForm(request.POST)
        email=form.data['email']
        username=form.data['username']
        password=form.data['password']
        valid=True
        errors={}
        context = getAllContext(request)
        #email validation
        pattern=re.compile('^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
        result=pattern.match(email)
        if result is None:
            errors.update({'email':'Valid email is required'})
            valid=False
        #validate email must not already registered
        if User.objects.filter(email=email).count()!=0 and not result is None:
            errors.update({'email':'Email already registered.'})
            valid=False
        # validation username must be unique
        if User.objects.filter(username=username).count()!=0 and not result is None:
            errors.update({'username':'Mobile already exist.'})
            valid=False

        # check valid mobile for username
        if not len(username)==10:
            errors.update({'username':'Mobile Number must consist of 10 digits.'})
            valid = False

        if not username.isdigit():
            errors.update({'username':'Invalid mobile number.'})
            valid = False

        #password validation
        if password == '':
            errors.update({'password':'Password is required'})
            valid=False

        #process the form if form is valid
        if valid is True:
            user = registerUser(email=email,password=password,username=username,usertype='customer')
            if user is not None:
                messages.success(request, 'Registration Successfull.')
                user.userprofile.userType = 'customer'
                user.userprofile.mobile = username
                user.userprofile.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('index')
            else:
                context['form'] = form
                context['errors'] = errors
                return render(request,"web/registration.html.j2",context)
        else:
            context['form'] = form
            context['errors'] = errors
            return render(request,"web/registration.html.j2",context)

def ServeCategory(request,slug):
    print("Catergory Slug--------------->",slug)
    """ to serve theme data """
    # context = {}
    context = getAllContext(request)
    category = Category.objects.get(slug=slug)
    context['category'] = category
    context['title'] = category.title_tag
    context['meta_desc'] = category.meta_description
    context['meta_keyword'] = category.meta_keyword
    context['long_contents'] = category.long_contents
    context['categories'] = Category.objects.all()
    context['gifting'] = GiftingCategory.objects.all().filter(gifting_type=category)
    context['promotional_banner'] = CategoryPagePromotionalBanner.objects.last()
    context['featured_plant'] = Plants.objects.filter(Q(category=category) | Q(category=category.parent_category),active=True, featured=True)[:8]
    plant = get_category_page_plants(category=category, page=1, num=8)
    context['plants'] = plant
    try:
        context['next_page'] = str(plant.next_page_number())
    except:
        context['next_page'] = 0
    return render(request, 'web/category.html.j2', context)



def ServeGifting(request,slug):
    print("Gifting SLUG------------>",slug)
    # return render(request, 'web/gifting.html.j2',{'key1':slug})
    """ to serve theme data """
    # context = {}
    context = getAllContext(request)
    category = Gifting.objects.get(slug=slug)
    print("Gifting Category------------->",category)
    context['category'] = category
    context['giftcategory'] = GiftingCategory.objects.all().filter(gifting_type=category)
    return context



def ServeGiftingCategoryProduct(request,slug):
    print("Product Slug------------------>",slug)
  
    context = getAllContext(request)
    category = GiftingCategory.objects.get(slug=slug)
    context['category'] = category
    context['giftproduct'] = Plants.objects.filter(giftcategory=category)
    print("GIFT PRODUCT --------->",context['giftproduct'])
    print("Gifting Category------------->",category)

    return render(request, 'web/giftproduct.html.j2',context)



def ServeGiftingProductDetails(request,slug):
    """ to serve theme data """
    print("Product Detail Slug -------------->",slug)
    # return render(request, 'web/giftproductdetail.html.j2',{'key1':slug})
    context = {}
    context = getAllContext(request)
    try:
        plant = GiftingCategoryProduct.objects.get(slug=slug,active=True)
    except Plants.DoesNotExist:
        raise Http404("This Plant does not exist")


    context['plant'] = plant
    cc = []
    # for p in context['plant'].category.all():
    #     cc.append(p)
    if plant.title_tag:
        context['title'] = plant.title_tag
    else:
        context['title'] = 'Buy '+plant.name
    context['meta_desc'] = plant.meta_description
    context['meta_keyword'] = plant.meta_keyword
    # context['plantQuestionAnswer'] = PlantQuestionAnswer.objects.filter(plant = context['plant'])
    # context['reviews'] = Review.objects.filter(plant = context['plant'], status='approved')
    context['plants'] = Plants.objects.filter(active=True,category__in=plant.category.all()).distinct()[:10]
    return render(request, 'web/giftproductdetail.html.j2', context)




def load_more_plants(request, **kwargs):
    """
    return more category
    """
    from django.http import JsonResponse
    slug = request.GET.get('slug')
    page = request.GET.get('page',1)
    try:
        category = Category.objects.get(slug=slug)
    except:
        return JsonResponse({"msg":"this category does not exist"}, safe=False, status=404)
    plant = get_category_page_plants(category=category, page=int(page), num=8)
    try:
        next_page = str(plant.next_page_number())
    except:
        next_page = 0
    data = get_template('web/sharable/more-category.html.j2').render({"request":request,"plants":plant,"page":next_page})
    return JsonResponse({"data":data,"next_page":next_page}, safe=False)






def ServePlant(request,slug):
    """ to serve theme data """
    print("Plant Details Slug -------------->",slug)
    # context = {}
    context = getAllContext(request)
    try:
        plant = Plants.objects.get(slug=slug,active=True)
    except Plants.DoesNotExist:
        raise Http404("This Plant does not exist")


    context['plant'] = plant
    cc = []
    # for p in context['plant'].category.all():
    #     cc.append(p)
    if plant.title_tag:
        context['title'] = plant.title_tag
    else:
        context['title'] = 'Buy '+plant.name
    context['meta_desc'] = plant.meta_description
    context['meta_keyword'] = plant.meta_keyword
    
    context['plantQuestionAnswer'] = PlantQuestionAnswer.objects.filter(plant = context['plant'])
    context['reviews'] = Review.objects.filter(plant = context['plant'], status='approved')
    context['plants'] = Plants.objects.filter(active=True,category__in=plant.category.all()).distinct()[:10]
    return render(request, 'web/plant.html.j2', context)

def ServeCart(request):
    """serve cart details"""
    # context = {}
    context = getAllContext(request)
    context['title'] = 'Cart Detail'
    context['meta_desc'] = 'Green Decor'
    context['meta_keyword'] = 'Green Decor'
    context['cartItems'] =  CartItem.objects.filter(cart=context['cart'])
    return render(request, 'web/cart.html.j2', context)


# @login_required
class ShippingView(View):
    """view class to handle the shipping process"""
    def get(self,request):
        """serve shipping page"""
        context = getAllContext(request)
        context['title'] = 'Shipping'
        context['meta_desc'] = 'Green Decor'
        context['meta_keyword'] = 'Green Decor'
        form=ShippingForm()
        context['form'] = form
        context['gift_wrap'] = request.GET.get('gift_wrap', '')
        context['errors'] = {}
        if CartItem.objects.filter(cart=context['cart']).count()==0:
            raise Http404("Your cart is empty")
        context['cartItems'] =  CartItem.objects.filter(cart=context['cart'])
        return render(request, 'web/shipping.html.j2', context)
    def post(self,request):
        context = getAllContext(request)
        user = user=request.user if request.user.is_authenticated else None
        cartItem =  CartItem.objects.filter(cart=context['cart'])
        form=ShippingForm(request.POST)
        gift_wrap = request.GET.get('gift_wrap', '')
        gift_text = request.GET.get('gift_text', '')
        # cartItem =  CartItem.objects.filter(cart=context['cart'])
        # plant_details = json.dumps(cartItem)
        # coupon_code = form.data['applied_coupon_code']
        try:
            discount = form.data['coupon_discount']
        except:
            discount = 0
        if not discount:
            discount = 0
        plant_details = []
        for item in cartItem:
            ss = {'plant':{'id':item.plant.id,'name':item.plant.name,'category':item.plant.category.name,'actual_price':item.plant.actual_price,'selling_price':item.plant.selling_price,'about':item.plant.about,'image':str(item.plant.images.all()[0].image)},'price':item.price,'quantity':item.quantity,'id':item.id}
            plant_details.append(ss)
        shipping_name = form.data['shipping_name']
        shipping_email = form.data['shipping_email']
        shipping_phone = form.data['shipping_phone']
        shipping_address1 = form.data['shipping_address1']
        shipping_address2 = form.data['shipping_address2']
        shipping_city = form.data['shipping_city']
        shipping_pincode = form.data['shipping_pincode']
        shipping_state = form.data['shipping_state']
        shipping_latitude = form.data['lat']
        shipping_longitude = form.data['lng']
        amount = form.data['amount']
        delivery_charge = form.data['delivery_charge']
        if gift_wrap=='true':
            is_gift = True
        else:
            is_gift = False
        booking = Booking.objects.create(
            user=user,
            plant_details=json.dumps(plant_details),
            amount=int(amount),
            coupon_discount=int(discount),
            shipping_name=shipping_name,
            shipping_phone=shipping_phone,
            shipping_email = shipping_email,
            shipping_address1=shipping_address1,
            shipping_address2=shipping_address2,
            shipping_city=shipping_city,
            shipping_pincode=shipping_pincode,
            shipping_state=shipping_state,
            is_gift=is_gift,
            gift_text=gift_text,
            shipping_latitude = float(shipping_latitude),
            shipping_longitude = float(shipping_longitude),
            delivery_charge=int(delivery_charge)
        )
        return redirect('/booking/'+str(booking.id)+'/payment')
        # return render(request, 'web/shipping.html.j2', context)


class AddPlantView(View):
    """view class to handle the add plant quantity for vendor"""
    # @login_required
    def get(self,request):
        """serve add plant form"""
        context = getAllContext(request)
        context['title'] = 'Add Plant Quantity'
        context['meta_desc'] = 'Green Decor'
        context['meta_keyword'] = 'Green Decor'
        form=AddPlantForm()
        context['form'] = form
        context['errors'] = {}
        context['cartItems'] =  CartItem.objects.filter(cart=context['cart'])
        return render(request, 'web/add-plant.html.j2', context)
    # @login_required
    def post(self,request):
        context = getAllContext(request)
        form=ShippingForm(request.POST)
        plant_id = form.data['plant']
        quantity = form.data['quantity']
        added, msg = add_plant_quantity(request,plant_id,quantity)
        if added:
            return redirect('/dashboard/my-plants/?msg='+msg)

        # if PlantStock.objects.filter(plant = plant,user=request.user).exists():
        #     ps = PlantStock.objects.get(plant = plant,user=request.user)
        #     ps.quantity = quantity
        #     ps.save()
        #     return redirect('/dashboard/my-plants/?msg=quantity successfully updated')
        # else:
        #     PlantStock.objects.create(plant = plant,user=request.user,quantity=quantity)
        #     return redirect('/dashboard/my-plants/?msg=successfull add plant stock')

@login_required
def MyPlantDetails(request):
    """serve my plants page"""
    context = getAllContext(request)
    context['title'] = 'My Plants'
    context['meta_desc'] = 'Green Decor'
    context['meta_keyword'] = 'Green Decor'
    context['items'] = PlantStock.objects.filter(user=request.user)
    return render(request, 'web/my-plants.html.j2', context)

@login_required
def delete_plant_stock(request,ps_id):
    """function for deleting plant stock"""
    if delete_plant_stock(request,ps_id):
        return HttpResponse('deleted')
    else:
        raise Http404("Stock does not exist")

# payment gateway
class PaymentView(View):
    def get(self,request,bid):
        context = getAllContext(request)
        booking = Booking.objects.get(id = bid)
        context['title'] = 'Make Payment'
        context['meta_desc'] = 'Green Decor'
        context['meta_keyword'] = 'Green Decor'
        context['booking'] = booking
        item = json.loads(booking.plant_details)
        context['plant_details'] = item
        return render(request, 'web/payment.html.j2', context)
    def post(self,request,bid):
        context = getAllContext(request)
        import hashlib
        import datetime
        try:
            booking = Booking.objects.get(id = bid)
        except Booking.DoesNotExist:
            raise Http404("Booking does not exist")
        # delivery_time = request.POST.get('delivery_time')
        payment_type = request.POST.get('payment_type')
        delivery_date = datetime.date.today() + datetime.timedelta(days=5)
        # delivery_date = request.POST.get('delivery_date')
        booking.payment_type = payment_type
        booking.delivery_date = delivery_date
        # booking.delivery_time = delivery_time
        booking.save()
        cartItem =  CartItem.objects.filter(cart=context['cart'])
        for item in cartItem:
            item.delete()
        if payment_type=='online_payu':
            #booking payment code
            # key='gtKFFx'
            # salt='eCwWELxi'
            key='w04qdosT'
            salt='8BQQdShyeJ'
            payee_name=request.user.username

            # if request.user.userprofile.mobile==None:
            #     payee_mobile=booking.shipping_phone
            # else:
            #     payee_mobile=request.user.userprofile.mobile
            # payee_email=request.user.email
            payee_mobile=booking.shipping_phone
            payee_email=booking.shipping_email
            invoice_id=''.join(random.choice('0123456789ABCDEF') for i in range(16))
            transaction=PaymentTransaction.objects.create(booking=booking,invoice_id=invoice_id,payee_name=payee_name,payee_email=payee_email,payee_mobile=payee_mobile,amount=booking.amount)
            hash_code=hashlib.sha512(key+'|'+invoice_id+'|'+str(transaction.amount)+'|'+str(transaction.id)+'|'+payee_name+'|'+payee_email+'|||||||||||'+salt).hexdigest()
            surl=settings.SERVER_ADDRESS+"booking/"+bid+"/success/"
            furl=settings.SERVER_ADDRESS+"booking/"+bid+"/failure/"
            curl=settings.SERVER_ADDRESS+"booking/"+bid+"/cancel/"
            return render(request, "payment/payment_payu.html.j2", {'transaction': transaction,'payee_name':payee_name,'payee_mobile':payee_mobile,'payee_email':payee_email,'key':key,'salt':salt, "hash_code":hash_code,"invoice_id":invoice_id,'surl':surl,'curl':curl,'furl':furl})
        else:
            return redirect('/booking/'+str(bid)+'/success')


def BookingSuccess(request, bid):
    """
    run after booking success
    :param request:
    :param bid:
    :return:
    """
    import pdfkit
    try:
        booking=Booking.objects.get(pk=bid)
    except Booking.DoesNotExist:
        raise Http404("Booking does not exist")
    booking.status = 'order_placed'
    booking.save()
    item = json.loads(booking.plant_details)
    if OrderDetails.objects.filter(order=booking).count()==0:
        for i in item:
            pl = Plants.objects.get(id = i['plant']['id'])
            order_detail = OrderDetails()
            order_detail.order = booking
            order_detail.plant = pl
            order_detail.quantity = i['quantity']
            order_detail.status = 'in_process'
            order_detail.save()
    subject = 'Order Placed'
    html_content = get_template('email_templates/order-placed.html.j2').render({
        'booking': booking,
        'title': 'Order Placed',
        'request': request,
        'item': item
    })
    html = get_template('email_templates/invoice.html.j2').render({
        'booking': booking,
        'title': 'Invoice',
        'request': request,
        'item': item
    })
    msg = EmailMessage(subject, html_content, DEFAULT_FROM_EMAIL, [booking.shipping_email])
    msg.content_subtype = "html"
    try:
        pdf = pdfkit.from_string(html, False)
        msg.attach('invoice.pdf', pdf, 'application/pdf')
    except:
        pass
    msg.send()
    html_content_admin = get_template('email_templates/order-mail-to-gd-admin.html.j2').render({'booking': booking, 'request': request, 'item': item})
    admin_emails = DEFAULT_TO_EMAIL
    send_email(subject='New Order', msg_body=html_content_admin, emails=admin_emails)
    m = 'Dear Customer,\
    Thank you for placing an order with Green Decor.Your order no- '+str(booking.id)+' has been received and will be processed soon.You may reach us @ 9953572573.'
    send_message(mobiles=booking.shipping_phone, message=m)
    return redirect('booking_success_page', bid=bid)


def BookingSuccessPage(request, bid):
    """
    return booking success page
    :param request:
    :param bid:
    :return:
    """
    context = getAllContext(request)
    try:
        booking = Booking.objects.get(pk=bid)
    except Booking.DoesNotExist:
        raise Http404("Booking does not exist")
    context['title'] = 'Payment Success'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    context['booking'] = booking
    item = json.loads(booking.plant_details)
    if OrderDetails.objects.filter(order=booking).count() == 0:
        for i in item:
            pl = Plants.objects.get(id=i['plant']['id'])
            order_detail = OrderDetails()
            order_detail.order = booking
            order_detail.plant = pl
            order_detail.quantity = i['quantity']
            order_detail.status = 'in_process'
            order_detail.save()
    context['plant_details'] = item
    context['data'] = request.POST
    return render(request, "payment/payment_success.html.j2", context)


def BookingFailure(request, bid):
    """handle booking failure"""
    try:
        booking = Booking.objects.get(pk=bid)
    except Booking.DoesNotExist:
        raise Http404("Booking does not exist")
    item = json.loads(booking.plant_details)
    subject = 'Order Failed'
    html_content = '<p>Your order failed.</p>'
    send_email(subject=subject,msg_body=html_content,emails=booking.shipping_email)
    # send admin mail
    html_content_admin = '<p>New Order failed.</p><p>Order Id: </p>' + str(booking.id) + ''
    send_email(subject='New Order Failed', msg_body=html_content_admin, emails=DEFAULT_TO_EMAIL)
    m = 'your order id '+str(booking.id)+' failed'
    send_message(mobiles=booking.shipping_phone, message=m)
    return redirect('booking_failure_page', bid=bid)


def BookingFailurePage(request, bid):
    """
    render payment failure page
    :param request:
    :param bid:
    :return:
    """
    context = getAllContext(request)
    try:
        booking = Booking.objects.get(pk=bid)
    except Booking.DoesNotExist:
        raise Http404("Booking does not exist")
    context['title'] = 'Payment Failed'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    context['booking'] = booking
    context['data'] = request.POST
    item = json.loads(booking.plant_details)
    context['plant_details'] = item
    return render(request, "payment/payment_failure.html.j2", context)


def BookingCancel(request,bid):
    """handle booking Cancel"""

    try:
        booking=Booking.objects.get(pk=bid)
    except Booking.DoesNotExist:
        raise Http404("Booking does not exist")
    item = json.loads(booking.plant_details)
    subject = 'Order Canceled'
    html_content = '<p>Your order cancelled.</p>'
    send_email(subject=subject, msg_body=html_content, emails=booking.shipping_email)
    # send admin mail
    html_content_admin = '<p>New Order Canceled.</p><p>Order Id: </p>' + str(booking.id) + ''
    send_email(subject='New Order Canceled', msg_body=html_content_admin, emails=DEFAULT_TO_EMAIL)
    m = 'your order id '+str(booking.id)+' cancelled'
    send_message(mobiles= booking.shipping_phone, message=m)
    return redirect('booking_cancel_page', bid=bid)


def BookingCancelPage(request, bid):
    """
    render booking cancel page
    :param request:
    :param bid:
    :return:
    """
    context = getAllContext(request)
    try:
        booking = Booking.objects.get(pk=bid)
    except Booking.DoesNotExist:
        raise Http404("Booking does not exist")
    context['title'] = 'Payment Cancel by user'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    context['booking'] = booking
    context['data'] = request.POST
    item = json.loads(booking.plant_details)
    context['plant_details'] = item
    return render(request, "payment/payment_cancel.html.j2", context)


def SocialLoginProfile(request):
    user=request.user
    email=user.email
    name=user.first_name+' '+user.last_name
    if UserProfile.objects.filter(user=user).count() == 0:
        UserProfile.objects.create(user=user, name=name, userType='customer')
    else:
        pass
    return redirect('/cart/')

def AddCart(request,plant,quantity):
    context = getAllContext(request)
    cart = context['cart']
    pl = Plants.objects.get(id=plant)
    if CartItem.objects.filter(plant = pl,cart=cart).count()==0:
        CartItem.objects.create(plant=pl,cart = cart,quantity=quantity,price =pl.selling_price)
    else:
        cart_item = CartItem.objects.get(plant = pl,cart=cart)
        cart_item.quantity = cart_item.quantity+1
        cart_item.save()
    return HttpResponse(CartItem.objects.filter(cart=cart).count())


def add_pot_to_cart(request,plant,quantity):
    """
    add pot to cart
    """
    context = getAllContext(request)
    cart = context['cart']
    try:
        pl = Plants.objects.get(id=plant)
    except Plants.DoesNotExist:
        return HttpResponse('This pot Does not exist', status=404)
    if CartItem.objects.filter(plant = pl,cart=cart).count()==0:
        CartItem.objects.create(plant=pl,cart = cart,quantity=quantity,price =pl.selling_price)
    else:
        pass
    return HttpResponse(CartItem.objects.filter(cart=cart).count())


def PlusCartItem(request,cartItemId):
    # context = getAllContext(request)
    # cart = context['cart']
    cart_item = CartItem.objects.get(id = cartItemId)
    cart_item.quantity = cart_item.quantity+1
    cart_item.save()
    return HttpResponse(cart_item.quantity)


def MinusCartItem(request,cartItemId):
    # context = getAllContext(request)
    # cart = context['cart']
    cart_item = CartItem.objects.get(id = cartItemId)
    cart_item.quantity = cart_item.quantity-1
    cart_item.save()
    return HttpResponse(cart_item.quantity)

def RemoveCartItem(request,cartItemId):
    # context = getAllContext(request)
    # cart = context['cart']
    cart_item = CartItem.objects.get(id = cartItemId)
    cart_item.delete()
    return HttpResponse('successfull removed')


@login_required
def Dashboard(request):
    """serve user dashboard page"""
    context = getAllContext(request)
    context['title'] = 'Dashboard'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    orders = Booking.objects.filter(user=request.user)
    o = []
    for order in orders:
        try:
            order.plant_details = json.loads(order.plant_details)
        except:
            pass
        o.append(order)
    context['orders'] = o
    return render(request, 'web/dashboard.html.j2', context)

def ContactUs(request):
    """serve contact us page"""
    if request.method == 'GET':
        context = getAllContext(request)
        context['title'] = 'Contact Us'
        context['meta_desc'] = ''
        context['meta_keyword'] = ''
        return render(request, 'web/contact.html.j2', context)
    if request.method == 'POST':
        # submit contsct form
        import requests
        res = request.POST['g-recaptcha-response']
        data = {"secret":"6LfOK4oUAAAAALXOl7OU9QeebAUh-DUTiy45KwC9", "response": res}
        try:
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            rsp = r.json()
            if rsp.get('success') is True:
                fname = request.POST['fname']
                lname = request.POST.get('lname','')
                email = request.POST['email']
                mobile = request.POST['phone']
                company_name = request.POST.get('company_name','')
                comment = request.POST.get('comment','')
                subject = "Thank you for contacting us"
                html_content = "<p>Thank you for contacting us. We will contact you soon<p><br/><br/><br/><br/><br/><p> Green Decor Team </p>"
                html_content_admin = "<p>Contact Us.</p><p>Name: "+fname+" "+lname+"</p><p>email: "+email+"</p><p>mobile: "+mobile+"</p><p>company name: "+company_name+"</p><p>message: "+comment+"</p><br/><br/><br/><br/><br/><p> Green Decor Team </p>"
                send_email(subject=subject,msg_body=html_content,emails=email)
                send_email(subject=subject,msg_body=html_content_admin,emails=DEFAULT_TO_EMAIL)
            else:
                pass
        except Exception as e:
            pass
        messages.success(request, 'Thank you for contacting us. We will contact you soon.')
        return redirect('index')


def Search(request):
    """serve search page"""
    context = getAllContext(request)
    context['title'] = 'Search Result'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    context['query'] = request.GET.get('query', '')
    context['plants'] = Plants.objects.filter(name__contains=context['query'],active=True)[:10]
    return render(request, 'web/search.html.j2', context)
def Faq(request):
    """serve FAQ page"""
    context = getAllContext(request)
    context['title'] = 'FAQ - Frequently Asked Qusestions about Green Decor'
    context['meta_desc'] = 'FAQ - Frequently Asked Qusestions about Green Decor.'
    context['meta_keyword'] = ''
    return render(request, 'web/faq.html.j2', context)

def UsersReview(request):
    """serve UsersReview page"""
    context = getAllContext(request)
    context['title'] = 'Users Review'
    context['meta_desc'] = 'Users Review'
    context['meta_keyword'] = ''
    return render(request, 'web/user-review.html.j2', context)

def AboutUs(request):
    """serve About us page"""
    context = getAllContext(request)
    context['title'] = 'Know About Team, Founder and Work Ethics of Green Decor'
    context['meta_desc'] = 'Explore Green Decor - the best online plant nursery based in Delhi. Get answer of questions like what we do, how we do and why you should choose us. Know about the team, founder and work-procedure of Green Decor.'
    context['meta_keyword'] = ''
    return render(request, 'web/about.html.j2', context)


def PrivacyPolicy(request):
    """serve PrivacyPolicy page"""
    context = getAllContext(request)
    context['title'] = 'Privacy Policy'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    return render(request, 'web/privacy-policy.html.j2', context)
def TermCondition(request):
    """serve TermCondition page"""
    context = getAllContext(request)
    context['title'] = 'Term Condition'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    return render(request, 'web/term-condition.html.j2', context)

def ForgotPassword(request):
    """serve TermCondition page"""
    context = getAllContext(request)
    context['title'] = 'Forgot Password'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    return render(request, 'web/forgot-password.html.j2', context)

@login_required
def MyOrderDetails(request,pk):
    """serve MyOrder Details page"""
    context = getAllContext(request)
    item = []
    context['title'] = 'Order Details'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    order = Booking.objects.get(pk=pk)
    context['order'] = order
    context['order_details'] = OrderDetails.objects.filter(order = order)
    jj = json.loads(order.plant_details)
    context['item'] = jj

    return render(request, 'web/my-order-details.html.j2', context)

@login_required
def MyOrder(request):
    """serve My Order List page"""
    context = getAllContext(request)
    context['title'] = 'Order List'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    orders = Booking.objects.filter(user=request.user)
    o = []
    for order in orders:
        try:
            order.plant_details = json.loads(order.plant_details)
        except:
            pass
        o.append(order)
    context['orders'] = o
    return render(request, 'web/my-order-list.html.j2', context)


class ChangePasswordView(View):
    """serve Change Password page"""
    def get(self, request):
        """get function for display change password form"""
        context = getAllContext(request)
        context['title'] = 'Change Password'
        context['meta_desc'] = ''
        context['meta_keyword'] = ''
        context['form'] = ChangePasswordForm()
        context['errors'] = {}
        return render(request, 'web/change-password.html.j2', context)
    def post(self, request):
        """post request for change password"""
        context = getAllContext(request)
        context['title'] = 'Change Password'
        errors={}
        form=ChangePasswordForm(request.POST)
        old_password=form.data['old_password']
        new_password=form.data['new_password']
        retype_password=form.data['retype_password']
        valid=True
        user=request.user
        #old password validation
        if old_password=='':
            errors.update({"old_password":"Old Password is required"})
            valid=False
        #old password validation
        if not user.check_password(old_password) and old_password!='':
            errors.update({"old_password":"Existing passsword is not correcct"})
            valid=False
        #new password validation
        if new_password=='':
            errors.update({"new_password":"Password is required"})
            valid=False
        #new password must not equal to old password
        if old_password==new_password and old_password!='':
            errors.update({"new_password":"New password must not equal to old password"})
            valid=False
        #retype password validation
        if retype_password=='':
            errors.update({"retype_password":"Retype your new password"})
            valid=False
        #retype password validation
        if new_password!=retype_password and new_password !='' and retype_password!='':
            errors.update({'retype_password':'Password and retype_password do not match'})
            valid=False
        #process form if condition met
        if valid == True:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password Changed Successfully.')
            context['title'] = 'Dashboard'
            return redirect('dashboard')
        context['form'] = form
        context['errors'] = errors
        return render(request, 'web/change-password.html.j2', context)


class MyProfileView(View):
    """docstring for MyProfileView."""
    def get(self, request):
        """get function for display profile form"""
        context = getAllContext(request)
        context['title'] = 'MyProfile'
        context['meta_desc'] = ''
        context['meta_keyword'] = ''
        context['form'] = UserProfileForm(instance=request.user.userprofile)
        context['errors'] = {}
        return render(request, 'web/my-profile.html.j2', context)
    def post(self,request):
        """post function for update profile form"""
        form=UserProfileForm(request.POST,instance=request.user.userprofile)
        if not form:
            raise Http404
        else:
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile Saved.')
                return redirect('/dashboard/')
                # return HttpResponse(json.dumps({"status": True, "msg": "Data saved successfully"}))
            else:
                # print form.errors
                context = getAllContext(request)
                context['title'] = 'My Address'
                context['form'] = form
                return render(request, 'web/my-profile.html.j2', context)

class MyAddressView(View):
    """docstring for MyAddressView."""
    def get(self, request):
        """get function for display user address form"""
        context = getAllContext(request)
        context['form'] = UserAddressForm(instance=request.user.userprofile)
        context['title'] = 'My Address'
        context['meta_desc'] = ''
        context['meta_keyword'] = ''
        return render(request, 'web/myaddress.html.j2', context)
    def post(self,request):
        """post function for update user address"""
        f = UserAddressForm(request.POST, instance=request.user.userprofile)
        if f.is_valid():
            f.save()
            messages.success(request, 'Address saved.')
            return redirect('/dashboard/')
        else:
            print f.errors
            context = getAllContext(request)
            context['title'] = 'My Address'
            context['form'] = f
            return render(request, 'web/myaddress.html.j2', context)


@login_required
def MyOrderWishlist(request):
    """serve My wishlist page"""
    context = getAllContext(request)
    context['title'] = 'MyOrderWishlist'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    return render(request, 'web/my-order-wishlist.html.j2', context)

@login_required
def AddPlant(request):
    """serve Add Plant"""
    context = getAllContext(request)
    context['title'] = 'Add Plant Quantity'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    context['plants'] = Plants.objects.filter(active=True)
    return render(request, 'web/add-plant.html.j2', context)

class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise ValidationError("There is no user registered with the specified email address!")
        return email

class PasswordValidationOnChangePassword(SetPasswordForm):
    def clean_new_password2(self):
        new_password2 = self.cleaned_data['new_password2']
        if not new_password2:
            raise ValidationError("=Confirm Password is required")
        try:
            new_password1 = self.cleaned_data['new_password1']
        except:
            new_password1 = ''
        if new_password1=='':
            return new_password2
        if not new_password1==new_password2:
            raise ValidationError("Password and confirm password do not match!")
        return new_password2



def PasswordResetView(request):
    context = getAllContext(request)
    return password_reset(request, template_name='password_reset/forgot_password.html.j2',
            email_template_name='password_reset/reset_password_email_template.html.j2',
            subject_template_name='password_reset/reset_password.txt',
            post_reset_redirect=reverse('reset_pasword_sent'),
            password_reset_form = EmailValidationOnForgotPassword,
            extra_email_context={'server_address':settings.SERVER_ADDRESS_WITHOUT_SLASH},
            extra_context={'title': 'Forgot Password','categories':Category.objects.all(),'cartCount':'0','delivery_charge_config':DeliveryChargeConfig.objects.all()[:1]})

def PasswordResetDoneVIew(request):
    context = getAllContext(request)
    context['title'] = 'Password Reset'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    return render(request,'password_reset/password_reset_done.html.j2',context)

def DoPasswordResetView(request, uidb64=None, token=None):
     return password_reset_confirm(request, template_name='password_reset/reset_password.html.j2',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('reset_pasword_complete'), set_password_form = PasswordValidationOnChangePassword,
        extra_context={'title': 'Forgot Password','meta_desc':'','meta_keyword':'','categories':Category.objects.all(),'delivery_charge_config':DeliveryChargeConfig.objects.all()[:1]})

def PasswordResetCompleteVIew(request):
    context = getAllContext(request)
    context['title'] = 'Password Reset'
    context['meta_desc'] = ''
    context['meta_keyword'] = ''
    return render(request,'password_reset/password_reset_complete.html.j2',context)


def check_coupon_code(request):
    code = request.GET.get('code')
    amount = request.GET.get('amount')
    try:
        coupon = Coupon.objects.get(code=code)
    except Coupon.DoesNotExist:
        return HttpResponse("Code does not exist",status=404)
    if coupon.is_redeemed:
        return HttpResponse("This code has already been used",status=400)

    if coupon.per_user_limit == 1:
        try:
            user_coupon = coupon.users.get(user=request.user)
            if user_coupon.redeemed_at is not None:
                return HttpResponse("This code has already been used by your account.",status=400)
        except CouponUser.DoesNotExist:
            if coupon.user_limit is not 0:  # zero means no limit of user count
                # only user bound coupons left and you don't have one
                if coupon.user_limit is coupon.users.filter(user__isnull=False).count():
                    return HttpResponse("This code is not valid for your account.",status=400)
                    # raise forms.ValidationError(_("This code is not valid for your account."))
                if coupon.user_limit is coupon.users.filter(redeemed_at__isnull=False).count():  # all coupons redeemed
                    return HttpResponse("This code has already been used.",status=400)
                    # raise forms.ValidationError(_("This code has already been used."))

    if coupon.per_user_limit == coupon.users.filter(user=request.user).count():
        return HttpResponse("This code has already been used by your account.",status=400)

    if coupon.expired():
        return HttpResponse("This code is expired.",status=400)
        # raise forms.ValidationError(_("This code is expired.")
    # return code
    if coupon.type == 'percentage':
        discount = (int(amount)*int(coupon.value))/100;
        if( discount>int(amount) and coupon.max_discount == 0):
            print 'if'
            return HttpResponse('coupon can not be applied',status=400)
        elif(int(coupon.max_discount) < discount and int(coupon.max_discount) > int(amount)):
            print 'elif'
            return HttpResponse('coupon can not be applied',status=400)
        if int(coupon.max_discount) !=0 and discount>int(coupon.max_discount):
            discount = int(coupon.max_discount)
        st = coupon.redeem(request.user)
    else:
        # discount = int(amount)-int(coupon.value)
        if int(coupon.value) > int(amount) and coupon.max_discount==0:
            return HttpResponse('coupon can not be applied',status=400)
        elif(int(coupon.max_discount) < int(coupon.value) and int(coupon.max_discount) > int(amount)):
            return HttpResponse('coupon can not be applied',status=400)
        if int(coupon.max_discount) !=0:
            discount = int(coupon.max_discount)
        else:
            discount = int(coupon.value)
        st = coupon.redeem(request.user)
    return HttpResponse(discount,status=200)



@login_required
def SaveReview(request,p_id):
    """
    Function of submit review
    """
    if request.method == 'POST':
        # write code here
        plant =   Plants.objects.get(id=p_id)
        review,rating,user = request.POST['review'],request.POST['rating'],request.user
        if Review.objects.filter(user=user,plant=plant).exists():
            rr = Review.objects.filter(user=user,plant=plant).first()
            rr.rating = int(rating)
            rr.review = review
            rr.save()
        else:
            r = Review.objects.create(review=review,rating=float(rating),user=user,plant=plant)
        return HttpResponse('success',status=200)
    else:
        return HttpResponse('Method not allowed',status=405)
        # something here



@login_required
def ApprovedOrderDetail(request,order_id):
    """
    Function of update status
    """
    if request.method == 'POST':
        try:
            order_detail =   OrderDetails.objects.get(id=order_id)
        except OrderDetails.DoesNotExist:
            raise Http404("Order does not exist")
        order_detail.status = 'customer_approval_done'
        order_detail.save()
        return HttpResponse('success',status=200)
    else:
        return HttpResponse('Method not allowed',status=405)

def GetInTouch(request):
    """
    function for sending get in touch mail
    """
    if request.method == 'POST':
        email = request.POST['email']
        html_content = "<p>Thank you for contacting us.</p><p>We will cotacting you soon.</p><br><br><br><br><p>Team Green Decor</p>"
        send_email(subject='Get In Touch',msg_body=html_content,emails=email)
        admin_content = "<p>New Contacts</p><p>Email: "+email+" </p>"
        send_email(subject='Get In Touch',msg_body=admin_content,emails=DEFAULT_TO_EMAIL)
        return HttpResponse("succes",status=200)
    else:
        return HttpResponse("Method not allowed",status=405)

from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def GetAdminInvoice(request,bid):
    """
    serve invoice in pdf
    """
    import pdfkit
    booking=Booking.objects.get(pk=bid)
    item = json.loads(booking.plant_details)
    html = get_template('email_templates/invoice.html.j2').render({'booking': booking,'title':'Invoice','request':request,'item':item})
    pdf = pdfkit.from_string(html, False)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Length'] = len(response.content)
    response['Content-Disposition'] = 'attachment; filename=invoice_%s.pdf' % booking.shipping_phone
    return response

def CorporateGifting(request, **kwargs):
    """
    serve CorporateGifting page
    """
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST.get('lname','')
        email = request.POST['email']
        mobile = request.POST['phone']
        company_name = request.POST.get('company_name','')
        comment = request.POST.get('comment','')
        subject = "New Message"
        # html_content = "<p>Thank you for contacting us. We will contact you soon<p><br/><br/><br/><br/><br/><p> Green Decor Team </p>"
        html_content_admin = "<p>New Message from</p><p>Name: "+fname+" "+lname+"</p><p>Email: "+email+"</p><p>Mobile: "+mobile+"</p><p>Company Name: "+company_name+"</p><p>Message: "+comment+"</p><br/><br/><br/><br/><br/><p> Green Decor Team </p>"
        # send_email(subject=subject,msg_body=html_content,emails=email)
        send_email(subject=subject,msg_body=html_content_admin,emails=DEFAULT_TO_EMAIL)
        send_email(subject=subject,msg_body=html_content_admin,emails='social@adhutmedia.com')
        messages.success(request, 'Thank you for contacting us. We will contact you soon.')
        return redirect('corporate-gifting-thanks')
    else:
        context = getAllContext(request)
        context['title'] = 'Corporate Green Gift Ideas for Employees and Clients, Buy Plants for Corporate Gifting - Green Decor'
        context['meta_desc'] = 'Choose eco-friendly corporate gift ideas for your employees and clients this festival. Buy high quality gift plants to give as corporate gifts online and opt for green gifting ideas with Green Decor - leading online plant nursery in India.'
        context['meta_keyword'] = 'Corporate Gift Ideas, Plants for Corporate Gift Ideas India, Gift Ideas for Employees India, Gift Ideas for Clients, Buy Plants for Corporate Gifts, Buy Plants for Corporate Gifting, Plants for Corporate Gifts, green gifts, eco friendly corporate gifts, green gifting idea in Delhi NCR, corporate gift plants'
        context['corporate_gift'] = CorporateGift.objects.all()
        return render(request, "web/corporate-gifting.html.j2", context)


def diwali_gifting_plants(request, **kwargs):
    """
    serve diwali gifting page
    """
    context = getAllContext(request)
    diwali_gifts = DiwaliGifts.objects.first()
    context['title'] = diwali_gifts.title
    context['meta_desc'] = diwali_gifts.description
    context['meta_keyword'] = diwali_gifts.keyword
    context['plants'] = diwali_gifts.plants.all()
    return render(request, "web/diwali-gifts.html.j2", context)


def CorporateGiftingThanks(request):
    """
    thank you page
    """
    context = getAllContext(request)
    context['title'] = 'GreenDecor.in - Buy plants, seeds & pots online in Delhi NCR'
    context['meta_desc'] = 'Greendecor is all about your plants & their needs. Buy Air Purifying Plants, Herbal Plants, Indoor Plants, Aromatic Plants, Bonsai Plants online in Delhi NCR'
    context['meta_keyword'] = 'Buy plants online in delhi, online plant nursery in delhi, buy plants online in gurgaon, online plant nursery in gurgaon, buy plants online in noida, online plant nursery in noida'
    return render(request, "web/corporate-gifting-thanks.html.j2", context)

def ShopPlantsOnlineView(request, **kwargs):
    """
    landing page for marketting shop-plants-from-online-nursery
    """
    context = getAllContext(request)
    page_data = OnlineNersery.objects.first()
    context['title'] = page_data.meta_title
    context['meta_desc'] = page_data.meta_description
    context['meta_keyword'] = page_data.meta_keyword
    context['page_data'] = page_data
    context['category_data'] = OnlineNerseryCategory.objects.all()
    return render(request, "web/online-nursery.html.j2", context)


def error_404_page(request, **kwargs):
    """
    serve 404 page
    """
    context = getAllContext(request)
    context['title'] = 'page not found'
    context['meta_desc'] = 'page you are looking for does not exist'
    context['meta_keyword'] = ''
    return render(request, "web/404.html.j2", context,status=404)


def error_500_page(request, **kwargs):
    """
    serve 404 page
    """
    context = getAllContext(request)
    context['title'] = 'server error'
    context['meta_desc'] = 'something wrong'
    context['meta_keyword'] = ''
    return render(request, "web/500.html.j2", context,status=500)




def RefundandCancellation(request):
    """serve About us page"""
    context = getAllContext(request)
    context['title'] = 'Know About Team, Founder and Work Ethics of Green Decor'
    context['meta_desc'] = 'Explore Green Decor - the best online plant nursery based in Delhi. Get answer of questions like what we do, how we do and why you should choose us. Know about the team, founder and work-procedure of Green Decor.'
    context['meta_keyword'] = ''
    return render(request, 'web/refund-and-cancellation.html.j2', context)