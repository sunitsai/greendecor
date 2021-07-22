# url here
from django.conf.urls import url, include
from .views import *
urlpatterns = [
    url(r'^plants/$',PlantsView.as_view(),name="get_all_plants"),
    url(r'^myplants/$',PlantsStockView.as_view(),name="get_my_plants"),
    url(r'^categories/$',CategoryView.as_view(),name="get_all_categories"),
    url(r'^register/$',UserView.as_view({'post': 'create_user'})),
    url(r'^login/$', UserView.as_view({'post': 'login_user'})),

    url(r'^add/plant/quantity/$', AddPlantView.as_view({'post': 'add_quantity'})),
    url(r'^delete/plantstock/(?P<ps_id>[0-9]+)/$', AddPlantView.as_view({'delete': 'delete_plant_stock'})),
    url(r'^plantstock/(?P<ps_id>[0-9]+)/$', AddPlantView.as_view({'get': 'get_plant_stock'})),
    url(r'^myprofile/$',ProfileView.as_view({'get': 'get_my_profile'})),
    url(r'^myprofile/update/$',ProfileView.as_view({'put': 'update_my_profile'})),
    url(r'^changePassword/$',ProfileView.as_view({'post': 'change_password'})),
    # forgot password Api
    url(r'^forgotPassword/$',ForgotPasswordView.as_view({'post': 'generate_code'})),
    url(r'^verifyCode/$',ForgotPasswordView.as_view({'post': 'verify_code'})),
    url(r'^resetpassword/$',ForgotPasswordView.as_view({'post': 'resetForgotPassword'})),
    # order details
    url(r'^myorders/$',OrderDetailsView.as_view(),name="get_all_orders"),
    # delivery boy OrdersView
    url(r'^myorders/delivery/$',DeliveryBoyOrdersView.as_view(),name="get_all_orders"),
    # change booking status delivery boy api
    url(r'^change/booking/status/(?P<booking_id>[0-9]+)/$',OrdersView.as_view({'put': 'update_booking_status'})),
    # upload order image
    url(r'^myorders/uploadimages/(?P<order_id>[0-9]+)/$',OrdersView.as_view({'post': 'uploadimages'})),
    # change order status vendor
    url(r'^myorders/(?P<order_id>[0-9]+)/$',OrdersView.as_view({'put': 'update_status'})),
]
