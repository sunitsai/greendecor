# @Author: Javed Ahamad
# @Date:   2017-02-12
# @Email:  javedahamad4@gmail.com
# @Filename: urls.py


from django.conf.urls import include, url
from .views import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required, permission_required
from core.models import *
from django.views.decorators.csrf import csrf_exempt

# {'title': 'Log In','categories':Category.objects.all()}}
urlpatterns = [
    url(r'^$', index,name='index'),
    url(r'^category/(?P<slug>[a-zA-Z0-9\-]+)/$', ServeCategory, name='category_details'),
    url(r'^gifting/(?P<slug>[a-zA-Z0-9\-]+)/$', ServeGifting, name='gifting_details'),
    url(r'^giftingproduct/(?P<slug>[a-zA-Z0-9\-]+)/$', ServeGiftingCategoryProduct, name='gifting_product'),
    url(r'^giftproductdetail/(?P<slug>[a-zA-Z0-9\-]+)/$', ServeGiftingProductDetails, name='gift_product_details'),
    # load mor plant
    url(r'^categoryplants/$', load_more_plants, name='get-more-category-plants'),
    url(r'^plant/(?P<slug>[a-zA-Z0-9\-]+)/$', ServePlant, name='plant_details'),
    url(r'^login/$',auth_views.login,{'template_name': 'web/login.html.j2','extra_context':{'title': 'Log In','meta_desc':'','meta_keyword':'','cartCount':'0','categories':Category.objects.all(),'delivery_charge_config':DeliveryChargeConfig.objects.all()[:1]}}, name='login'),
    url(r'^register/$',RegisterView.as_view(), name='register'),
    #for social login
    url(r'^login/social/$',SocialLoginProfile,name='social_login_profile'),
    url(r'^logout/$',auth_views.logout, {'next_page': '/'},name='logout'),
    url(r'^addcart/(?P<plant>[0-9]+)/(?P<quantity>[0-9]+)/$', AddCart,name='add_to_cart'),
    url(r'^addsuplementrypot/(?P<plant>[0-9]+)/(?P<quantity>[0-9]+)/$', add_pot_to_cart, name='add_pot_to_cart'),

    url(r'^increaseQuantity/(?P<cartItemId>[0-9]+)/$', PlusCartItem,name='increaseQuantity'),
    url(r'^decreaseQuantity/(?P<cartItemId>[0-9]+)/$', MinusCartItem,name='decreaseQuantity'),
    url(r'^removeCart/(?P<cartItemId>[0-9]+)/$', RemoveCartItem,name='removeItem'),

    url(r'^cart/$', ServeCart,name='cart'),
    # url(r'^shipping/$', login_required(ShippingView.as_view()),name='shipping'),
    url(r'^shipping/$', ShippingView.as_view(),name='shipping'),
    # url(r'^booking/(?P<bid>[0-9]+)/payment/$', login_required(PaymentView.as_view()),name='payment'),
    url(r'^booking/(?P<bid>[0-9]+)/payment/$', PaymentView.as_view(),name='payment'),


    # user for payu return
    url(r'^booking/(?P<bid>[0-9]+)/success/$',csrf_exempt(BookingSuccess),name='booking_success'),
    url(r'^booking/(?P<bid>[0-9]+)/failure/$',csrf_exempt(BookingFailure),name='booking_failure'),
    url(r'^booking/(?P<bid>[0-9]+)/cancel/$',csrf_exempt(BookingCancel),name='booking_cancel'),

    # render pages
    url(r'^booking/success/(?P<bid>[0-9]+)/$', BookingSuccessPage, name='booking_success_page'),
    url(r'^booking/failure/(?P<bid>[0-9]+)/$', BookingFailurePage, name='booking_failure_page'),
    url(r'^booking/cancel/(?P<bid>[0-9]+)/$', BookingCancelPage, name='booking_cancel_page'),


    # forgot password functionality
    url(r'^reset/password/$',PasswordResetView,name='reset_pasword_do'),
    url(r'^reset/password/sent/$',PasswordResetDoneVIew,name='reset_pasword_sent'),
    url(r'^reset/password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/do/$',DoPasswordResetView,name='reset_pasword_do'),
    url(r'^reset/password/done/$',PasswordResetCompleteVIew,name='reset_pasword_complete'),


    url(r'^dashboard/$', Dashboard,name='dashboard'),
    url(r'^contact-us/$', ContactUs,name='contact-us'),
    url(r'^faq/$', Faq,name='faq'),
    url(r'^about-us/$', AboutUs,name='about-us'),
    url(r'^search/$', Search,name='search'),
    url(r'^privacy-policy/$', PrivacyPolicy,name='privacy-policy'),
	url(r'^usersreview/$', UsersReview,name='user-review'),
    url(r'^term-condition/$', TermCondition,name='term-condition'),
    url(r'^forgot-password/$', ForgotPassword,name='forgot-password'),
    url(r'^dashboard/order/(?P<pk>[0-9]+)/$', MyOrderDetails,name='my-order-details'),
    url(r'^dashboard/my-orders/$', MyOrder,name='my-orders'),
    url(r'^dashboard/change-password/$', login_required(ChangePasswordView.as_view()),name='change-password'),
    url(r'^dashboard/my-profile/$', login_required(MyProfileView.as_view()),name='my-profile'),
    url(r'^dashboard/my-address/$', login_required(MyAddressView.as_view()),name='my-address'),
    url(r'^dashboard/my-wishlist/$', MyOrderWishlist,name='my-wishlist'),
    url(r'^dashboard/add-plant/$', login_required(AddPlantView.as_view()),name='add-plant'),
    url(r'^dashboard/my-plants/$', MyPlantDetails,name='my-plants'),
    url(r'checkcouponcode/$', check_coupon_code),
    # Approved order image
    url(r'^approved/order/(?P<order_id>[0-9]+)/$', ApprovedOrderDetail, name='approve-order'),

    # submit Review
    url(r'^savereview/(?P<p_id>[0-9]+)/$', SaveReview,name='save-review'),
    url(r'^getintouch/$', GetInTouch,name='get-in-touch'),
	
	
    # serve invoice
    url(r'^admin/booking/(?P<bid>[0-9]+)/invoice/$', GetAdminInvoice,name='get-admin-invoice'),

    # CorporateGifting old url
    # url(r'^corporate-gifting/$', CorporateGifting,name='corporate-gifting'),

    # updated corporate gifting page url
    url(r'^buy-plants-for-corporate-gifting/$', CorporateGifting,name='corporate-gifting'),
    url(r'^buy-plants-for-diwali-gifts/$', diwali_gifting_plants,name='diwali-gifting-plants'),

    url(r'^corporate-gifting/thank-you$', CorporateGiftingThanks,name='corporate-gifting-thanks'),
    # new landing page for marketting shop-plants-from-online-nursery
    url(r'^shop-plants-from-online-nursery/$', ShopPlantsOnlineView,name='shop-plants-from-online-nursery'),

]
