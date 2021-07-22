from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *
from rest_framework.fields import CurrentUserDefault


class UserSerializer(serializers.ModelSerializer):
    """docstring forUserSerializer."""
    class Meta:
        model = User
        fields = ('id','username','email')

class TagSerializers(serializers.Serializer):
    """Serializers class for serialize Tags"""
    name = serializers.CharField(max_length=100)

class SeasonSerializers(serializers.Serializer):
    """Serializers class for serialize Season"""
    name = serializers.CharField(max_length=100)


class BenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        fields = '__all__'

class ImagesSerializer(serializers.Serializer):
    # class Meta:
    #     model = Images
    #     fields =('id','image')
    pk = serializers.IntegerField()
    image =serializers.CharField(max_length=250)

class ProfileSerializer(serializers.Serializer):
    """
    get serialize profile data.
    """
    id = serializers.IntegerField(required=False)
    userType = serializers.CharField(max_length=250,required=False,read_only=True)
    user = UserSerializer(many=False, read_only=True)
    mobile = serializers.CharField(max_length=10,required=False,allow_blank=True)
    date_of_birth = serializers.DateField(required=False)
    name = serializers.CharField(allow_blank=True,max_length=200,required=False)
    address_line1 = serializers.CharField(allow_blank=True,max_length=250,required=False)
    address_line2 = serializers.CharField(allow_blank=True,max_length=250,required=False)
    state = serializers.CharField(allow_blank=True,max_length=100,required=False)
    city = serializers.CharField(allow_blank=True,max_length=100,required=False)
    nearest_landmark = serializers.CharField(allow_blank=True,max_length=250,required=False)
    pincode = serializers.IntegerField(required=False)
    latitude = serializers.FloatField(required=False)
    longitude = serializers.FloatField(required=False)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.mobile = validated_data.get('mobile', instance.mobile)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.name = validated_data.get('name', instance.name)
        instance.address_line1 = validated_data.get('address_line1', instance.address_line1)
        instance.address_line2 = validated_data.get('address_line2', instance.address_line2)
        instance.state = validated_data.get('state', instance.state)
        instance.city = validated_data.get('city', instance.city)
        instance.nearest_landmark = validated_data.get('nearest_landmark', instance.nearest_landmark)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.save()
        return instance



class VendorSerializer(serializers.ModelSerializer):
    """docstring forUserSerializer."""
    userprofile = ProfileSerializer(many=False, read_only=True)
    class Meta:
        model = User
        fields = ('email','userprofile')


class CategorySerializer(serializers.ModelSerializer):
    benefits = BenefitsSerializer(many=True, read_only=True)
    banner_images = ImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = '__all__'

class PlantsSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=False, read_only=True)
    # benefits = BenefitsSerializer(many=True, read_only=True)
    images = ImagesSerializer(many=True, read_only=True)
    class Meta:
        model = Plants
        fields = ('id','name','images')

class PlantDetailsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    # benefits = BenefitsSerializer(many=True, read_only=True)
    images = ImagesSerializer(many=True, read_only=True)
    tags = TagSerializers(many=True, read_only=True)
    season = SeasonSerializers(many=True, read_only=True)
    class Meta:
        model = Plants
        fields = '__all__'

class PlantStockSerializer(serializers.ModelSerializer):
    """docstring for PlantStockSerializer."""
    plant = PlantsSerializer(many=False,read_only=True)
    class Meta:
        model = PlantStock
        fields = ('id','plant','quantity')

class PlantStockDetailsSerializer(serializers.ModelSerializer):
    """docstring for PlantStockSerializer."""
    plant = PlantDetailsSerializer(many=False,read_only=True)
    class Meta:
        model = PlantStock
        fields = ('id','plant','quantity')


class OrderSerializers(serializers.ModelSerializer):
    """docstring for OrderSerializers."""
    plant = PlantsSerializer(many=False,read_only=True)
    images = ImagesSerializer(many=True, read_only=True)
    class Meta:
        model = OrderDetails
        fields = ('id','order','plant','images','quantity','status')

class DeliveryOrderSerializers(serializers.ModelSerializer):
    """docstring for OrderSerializers."""
    plant = PlantsSerializer(many=False,read_only=True)
    vendor = VendorSerializer(many=False,read_only=True)
    class Meta:
        model = OrderDetails
        fields = ('id','vendor','plant','quantity','status')


class DeliveryBoyBooking(serializers.Serializer):
    """
    docstring forDeliveryBoyBooking.
    """
    id = serializers.IntegerField(required=False)
    orderdetails = serializers.SerializerMethodField('order_details')
    status = serializers.CharField(max_length=100)
    customer = serializers.SerializerMethodField('customer_details')
    shipping_name = serializers.CharField(max_length=150)
    shipping_phone = serializers.CharField(max_length=150)
    shipping_address1 = serializers.CharField(max_length=150)
    shipping_address2 = serializers.CharField(max_length=150)
    shipping_state = serializers.CharField(max_length=150)
    shipping_city = serializers.CharField(max_length=150)
    shipping_pincode = serializers.CharField(max_length=150)
    shipping_latitude = serializers.FloatField()
    shipping_longitude = serializers.FloatField()
    delivery_date = serializers.DateField()

    def customer_details(self,obj):
        """
        get customer details
        """
        return VendorSerializer(obj.user).data

    def order_details(self,obj):
        """
        function for getting order details
        """
        order_details = OrderDetails.objects.filter(order = obj)
        orders = []
        for od in order_details:
            n= DeliveryOrderSerializers(od).data
            orders.append(n)
        return orders
