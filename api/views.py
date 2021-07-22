
from django.shortcuts import render
from rest_framework import filters
import django_filters
from rest_framework import generics
from django.contrib.auth.models import User
from core.models import *
from core.serializers import *
from core.utils import *
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from django.core import serializers
from rest_framework.parsers import JSONParser
from greenDecor import settings
from django.core.mail import send_mail
import string
import random



class UserView(viewsets.ViewSet):
    def check_username(self, request):
        """
        Get function for checking username
        """
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response(data={'status': False, 'msg': 'user already exists'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'status': True, 'msg': 'user Available'},status=status.HTTP_200_OK)

    def check_email(self, request):
        """
        Get function for checking email
        """
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response(data={'status': False, 'msg': 'email id already exists'},status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'status': True, 'msg': 'email Available'},status=status.HTTP_200_OK)

    def login_user(self, request):
        """
        Function for authenticate user
        """
        username = request.data.get('username')
        password = request.data.get('password')
        # get the authentication status
        authenticated, current_user = authenticate_user(username, password)
        # if not authenticated successfully
        if not authenticated:
            return Response(data={'status': False,'msg': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
        elif current_user.userprofile.userType == 'customer':
            return Response(
                data={'status': False, 'msg': 'User not autherized'},
                status=status.HTTP_401_UNAUTHORIZED)
        else:
            # authenticated successfully, generate token
            current_token = Token.objects.get_or_create(user=current_user)
            return Response(data={'status': True,'msg': 'User Authenticated successfully', 'token': str(current_token[0]),'usertype':current_user.userprofile.userType},
                            status=status.HTTP_200_OK)

    def create_user(self,request):
        """
        Get function for create user
        """
        username = request.data.get('username')
        usertype = request.data.get('usertype','vendor')
        email = request.data.get('email')
        password = request.data.get('password')
        if usertype !='delivery_boy' and usertype !='vendor':
            return Response(data={'status': False, 'msg': 'Invalid usertype'},status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response(data={'status': False, 'msg': 'Mobile number already exists'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response(data={'status': False, 'msg': 'email id already exists'},status=status.HTTP_400_BAD_REQUEST)

        if not len(username)==10:
            return Response(data={'status': False, 'msg': 'Mobile number must consist of 10 digits.'},status=status.HTTP_400_BAD_REQUEST)
        if not username.isdigit():
            return Response(data={'status': False, 'msg': 'Invalid mobile number'},status=status.HTTP_400_BAD_REQUEST)

        user = registerUser(email=email,password=password,username=username)
        if user is not None:
            user.userprofile.userType = usertype
            user.userprofile.mobile = username
            user.userprofile.save()
            current_token = Token.objects.get_or_create(user=user)
            return Response(data={'status': True,'token':str(current_token[0]), 'msg':'User created successfully','usertype':user.userprofile.userType},status=status.HTTP_200_OK)

class ProfileView(viewsets.ViewSet):
    """docstring for ProfileView."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def get_my_profile(self,request):
        """
        Get function for get user profile
        """
        data = ProfileSerializer(UserProfile.objects.get(user=request.user)).data
        return Response(data={'status': True, 'profile':data},status=status.HTTP_200_OK)

    def update_my_profile(self,request):
        """
        Put function for update user profile
        """
        userprofile = UserProfile.objects.get(user=request.user)
        data = JSONParser().parse(request)
        serializer = ProfileSerializer(userprofile, data = data)
        if serializer.is_valid():
            dd = serializer.save()
            return Response(data={'status': serializer.is_valid(), 'profile':ProfileSerializer(dd).data},status=status.HTTP_200_OK)
        else:
            return Response(data={'status': serializer.is_valid(), 'errors':serializer.errors},status=status.HTTP_400_BAD_REQUEST)


    def change_password(self, request):
        current_data = request.data
        old_password = current_data.get('old_password')
        new_password = current_data.get('new_password')
        confirm_password = current_data.get('confirm_password')
        user = request.user
        if new_password != confirm_password:
            return Response(data={'status':False, 'message':'Password mismatch'},status=status.HTTP_400_BAD_REQUEST)
        if len(new_password) < 6:
            return Response(data={'status':False, 'message':'The password must contain atleast 6 characters'},status=status.HTTP_400_BAD_REQUEST)
        if old_password == new_password:
            return Response(data={'status':False, 'message':'New password and old password can not be same'},status=status.HTTP_400_BAD_REQUEST)
        if user.check_password(old_password):
            u = User.objects.get(id=request.user.id)
            u.set_password(new_password)
            u.save()
            return Response(data={'status':True, 'message':'Password changed'},status=status.HTTP_200_OK)
        else:
            return Response(data={'status':False, 'message':'Old password  did not match'},status=status.HTTP_400_BAD_REQUEST)

def generate_random_code(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))
class ForgotPasswordView(viewsets.ViewSet):
    def generate_code(self, request):
        """Function to generate the otp send it to the user as well as set it for the user"""
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(data={'status': False, 'msg': 'Email does not exist'},
                            status=status.HTTP_404_NOT_FOUND)

        code = generate_random_code()
        user.userprofile.forgot_code=code
        user.userprofile.save()
        try:
            email = request.data.get('email')
            template_email_text = 'Forgot Passwor verification code:  '+code
            send_mail('Green Decor! Forgot Password', template_email_text, settings.DEFAULT_FROM_EMAIL, [email],
                  fail_silently=False,html_message="<html><body><h2>Hi "+user.username+",</h2><p>To reset the password for your Green Decor account, please enter the following code:<br/>"+code+"</p><p><br/><br/><b>Team Green Decor</b></p><p><br/><br/>This is an automated email, please don't reply</p></body></html>")
        except Exception as e:
            return Response(data={'status': False, 'msg': e.message},status=status.HTTP_400_BAD_REQUEST)

        return Response(data={'status': True, 'msg': 'Forgot password verification code send to your email '},status=status.HTTP_200_OK)

    def verify_code(self, request):
        """function to verify the orp if it exists in the db"""
        try:
            code = request.data.get('code')
            email = request.data.get('email')
        except:
            return Response(data={'status': False, 'msg': 'code and email both required'},
                            status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        try:
            user = User.objects.get(email = email)
        except:
            return Response(data={'status': False, 'msg': 'email not exist'},
                            status=status.HTTP_404_NOT_FOUND)
        if UserProfile.objects.filter(user = user, forgot_code = code).exists():
            return Response(data={'status': True, 'msg': 'code exists'},status=status.HTTP_200_OK)
        else:
            return Response(data={'status': False, 'msg': 'code not exists'},status=status.HTTP_404_NOT_FOUND)

    def resetForgotPassword(self, request):
        """function to chab=nge the password of the user based on the pin and mobile provided"""
        try:
            code = request.data.get('code')
            email = request.data.get('email')
        except:
            return Response(data={'status': False, 'msg': 'email and code are required!'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email = email)
        except:
            return Response(data={'status': False, 'msg': 'email not exist'},status=status.HTTP_404_NOT_FOUND)
        if not UserProfile.objects.filter(user = user, forgot_code = code).exists():
            return Response(data={'status': False, 'msg': 'code not exist'},status=status.HTTP_404_NOT_FOUND)
        try:
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')
        except:
            return Response(data={'status': False, 'msg': 'new_password and confirm_password required both'},status=status.HTTP_400_BAD_REQUEST)
        if not new_password:
            return Response(data={'status': False, 'msg': 'new_password and confirm_password required both'},status=status.HTTP_400_BAD_REQUEST)
        if not new_password == confirm_password:
            return Response(data={'status': False, 'msg': 'new_password and confirm_password do not match'},
                            status=status.HTTP_400_BAD_REQUEST)
        # reset password code here
        user.set_password(new_password)
        user.save()
        user.userprofile.forgot_code=''
        user.userprofile.save()
        return Response(data={'status': True, 'msg': 'password changed successfully'},status=status.HTTP_200_OK)



class AddPlantView(viewsets.ViewSet):
    """docstring for Add Plant Quan-tity."""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    def add_quantity(self,request):
        """
        Get function for add plant quantity
        """
        if request.user.userprofile.userType == 'customer':
            return Response(
                data={'status': False, 'msg':'You are not authorized.'},status=status.HTTP_401_UNAUTHORIZED)
        plant_id = request.data.get('plant_id')
        quantity = request.data.get('quantity')
        added, msg = add_plant_quantity(request,plant_id,quantity)
        if added:
            return Response(data={'status': added, 'message':msg},status=status.HTTP_200_OK)

    def delete_plant_stock(self, request,ps_id):
        """
        Get function for deleting plant stock
        """
        deleted = delete_plant_stock(request,ps_id)
        if deleted:
            return Response(data={'status': True, 'msg':'stock deleted'},status=status.HTTP_200_OK)
        else:
            return Response(data={'status': False, 'msg':'stock does not exist'},status=status.HTTP_404_NOT_FOUND)

    def get_plant_stock(self,request,ps_id):
        """
        Get function for deleting plant stock
        """
        try:
            p = PlantStockDetailsSerializer(PlantStock.objects.get(id=ps_id)).data
            return Response(data={'status': True, 'stock':p},status=status.HTTP_200_OK)
        except:
            return Response(data={'status': False, 'msg':'stock does not exist'},status=status.HTTP_404_NOT_FOUND)


class OrdersView(viewsets.ViewSet):
    """
    docstring for OrdersView.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializers
    def uploadimages(self,request,order_id):
        images = request.data.get('images')
        try:
            od = OrderDetails.objects.get(id=order_id)
        except:
            return Response(data={'status': False, 'msg': 'Order not exist'},status=status.HTTP_404_NOT_FOUND)

        for i in images:
            od.images.add(Images.objects.create(image=i['image']))
            od.save()
        od.status = 'pending_customer_approval'
        od.save()
        html_content = '<p>Approve product '+ od.plant.name +'.</p><p>Order Id: '+ str(od.order.id) +'</p>'
        send_email(subject='Approved Product',msg_body=html_content,emails=od.order.user.email)
        m = 'approved product '+ od.plant.name +' Order id '+str(od.order.id)+''
        send_message(mobiles=od.order.shipping_phone,message=m)
        return Response(data={'status': True, 'msg':'image uploaded'},status=status.HTTP_200_OK)

    def update_status(self,request,order_id):
        """
        function for update order status
        """
        s = request.data.get('status')
        try:
            od = OrderDetails.objects.get(id=order_id)
        except:
            return Response(data={'status': False, 'msg': 'Order not exist'},status=status.HTTP_404_NOT_FOUND)
        if s == '' or s==None:
            return Response(data={'status': False, 'msg': 'status required'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        od.status = s
        od.save()
        return Response(data={'status': True, 'msg':'status changed'},status=status.HTTP_200_OK)


    def update_booking_status(self,request,booking_id):
        """
        function for update order status
        """
        s = request.data.get('status')
        try:
            bk = Booking.objects.get(id=booking_id)
        except:
            return Response(data={'status': False, 'msg': 'Booking not exist'},status=status.HTTP_404_NOT_FOUND)
        if s == '' or s==None:
            return Response(data={'status': False, 'msg': 'status required'},status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        bk.status = s
        bk.save()
        trigger_mail(s,bk)
        return Response(data={'status': True, 'msg':'status changed'},status=status.HTTP_200_OK)



class OrderDetailsView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializers
    def get_queryset(self):
        return OrderDetails.objects.filter(vendor=self.request.user)


class PlantsStockView(generics.ListAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = PlantStockSerializer
    def get_queryset(self):
        return PlantStock.objects.filter(user=self.request.user)


class PlantsView(generics.ListAPIView):
    queryset = Plants.objects.all()
    serializer_class = PlantsSerializer

class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class DeliveryBoyOrdersView(generics.ListAPIView):
    """
    docstring forDeliveryBoyOrdersView.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeliveryBoyBooking
    def get_queryset(self):
        return Booking.objects.filter(deliveryboyorder__delivery_boy=self.request.user)
