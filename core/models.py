# @Author: Javed Ahamad
# @Date:   2017-02-14
# @Email:  javedahamad4@gmail.com
# @Filename: core/models.py

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from location_field.models.spatial import LocationField
from django.contrib.auth.models import User
from jsonfield import JSONField
from datetime import date
from datetime import datetime
from coupon.models import Coupon, CouponUser, Campaign
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from django.core.validators import MaxValueValidator,MinValueValidator, ValidationError

class Base(models.Model):
    class Meta:
        abstract=True


class Images(Base):
    """docstring for Images"""
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=150,blank=True,null= True, default=None)
    alt = models.CharField(max_length=150,blank=True,null= True, default=None)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')


class Benefit(Base):
    """docstring for Benefit"""
    title = models.CharField(max_length=150,null= True, default=None)
    icon = models.ImageField(upload_to='images/')
    def __unicode__(self):
        return '{}'.format(self.title)

class Tags(Base):
    """docstring for Tags."""
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return '{}'.format(self.name)
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

class Season(Base):
    """docstring for Season."""
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return '{}'.format(self.name)
    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Season'

class MaintenanceLevel(Base):
    """docstring for MaintenanceLevel."""
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return '{}'.format(self.name)
    class Meta:
        verbose_name = 'Maintenance Level'
        verbose_name_plural = 'Maintenance Level'




class Category(Base):
    """docstring for Category"""
    TYPE_CHOICES = (
        ('Plants','Plants'),
        ('Accessories','Accessories'),
        ('Gifting','Gifting')

    )
    name = models.CharField(max_length=150,null= True, default=None)
    slug = models.SlugField(max_length=200, null=True,blank=True,unique=True,default=None)
    banner_images = GenericRelation(Images)
    banner_text = models.TextField(max_length=500,null= True, default=None)
    feature_text = models.TextField(max_length=500,null= True, default=None)
    thumbnail = models.ImageField(upload_to='images/',default='images/product-image.jpg')
    description = models.TextField(max_length=1000,null= True, default=None)
    parent_category = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE)
    benefits = models.ManyToManyField(Benefit)
    synonyms = models.CharField(max_length=250,null=True,blank=True,default=None)
    title_tag = models.CharField(max_length=500,blank=True,null= True)
    meta_description = models.CharField(max_length=500,blank=True,null= True, default=None)
    meta_keyword = models.CharField(max_length=500,blank=True,null= True, default=None)
    long_contents = models.TextField(max_length=25000,blank=True,null= True, default=None)
    video_url = models.URLField(max_length=500,null=True,default=None)
    category_type = models.CharField(max_length=50,choices=TYPE_CHOICES,default='Plants')
    custom_header_meta = models.CharField(max_length=2000,null= True, blank=True, default=None)
    custom_script_seo = models.CharField(max_length=2000,null= True, blank=True, default=None)

    def __unicode__(self):
        return '{}'.format(self.name)
    def save(self, *args, **kwargs):
        s = slugify(self.name)
        if self.slug==None or self.slug=='':
            self.slug = 'buy-'+s+'-online-in-delhi'
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'



class GiftingCategory(Base):
    gifting_type = models.ForeignKey(Category,on_delete=models.CASCADE)
    parent_category = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=500)
    slug = models.SlugField(max_length=200, null=True,blank=True,unique=True,default=None)
    description = models.TextField(max_length=1000,null= True, default=None)
    thumbnail = models.ImageField(upload_to='images/',default='images/product-image.jpg')

    def __unicode__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = 'GiftingCategory'
        verbose_name_plural = 'GiftingCategories'


class PriceCategory(Base):
    """docstring for PriceCategory"""
    name = models.CharField(max_length=150,null= True, default=None)
    def __unicode__(self):
        return '{}'.format(self.name)
    class Meta:
        verbose_name = 'Price Category'
        verbose_name_plural = 'Price Categories'

class Plants(Base):
    """docstring for Plants."""
    CHOICE=(
        ('Outdoor-Sunny','Outdoor-Sunny'),
        ('Outdoor-Shades','Outdoor-Shades'),
        ('Indoor','Indoor'),
        ('Outdoor-Sunny or Indoor','Outdoor-Sunny or Indoor'),
        ('Outdoor-Shades or Indoor','Outdoor-Shades or Indoor'),
        ('Anywhere','Anywhere')
    )
    FRAGRANCE = (
        ('Strong','Strong'),
        ('Low','Low'),
        ('Medium','Medium'),
        ('None','None')
    )
    WATER = (
        ('Alternate Day','Alternate Day'),
        ('Daily','Daily'),
        ('Twice Week','Twice Week'),
        ('Weekly','Weekly'),
        ('Monthly','Monthly'),
    )
    FERTILIZER = (
        ('Every Month','Every Month'),
        ('1-2 Month','1-2 Month'),
        ('2-3 Month','2-3 Month'),
        ('3-4 Month','3-4 Month'),
        ('4-5 Month','4-5 Month'),
        ('5-6 Month','5-6 Month'),
        ('6-7 Month','6-7 Month'),
        ('7-8 Month','7-8 Month'),
        ('8-9 Month','8-9 Month'),
        ('9-10 Month','9-10 Month'),
        ('No','No'),
    )
    PLANT_TYPE_CHOICES = (
        ('Fruit','Fruit'),
        ('Vegetable','Vegetable'),
        ('None','None'),
    )
    PRODUCT_TYPE_CHOICES = (
        ('Plants','Plants'),
        ('Seeds','Seeds'),
        ('Pots','Pots'),
        ('Tools','Tools'),
        ('Fertilizers','Fertilizers'),
        ('Soil','Soil'),
        ('Combos','Combos'),
        ('Organic Compose','Organic Compose'),
        ('Organic Compose','Organic Compose'),
        ('GiftingCategory','GiftingCategory'),
    )
    POT_SIZE_CHOICES = (
        (4,'4"'),
        (5,'5"'),
        (6,'6"'),
        (7,'7"'),
        (8,'8"'),
        (9,'9"'),
        (10,'10"'),
        (11,'11"'),
        (12,'12"'),
        (13,'13"'),
        (14,'14"'),
        (15,'15"'),
        (16,'16"'),
        (17,'17"'),
        (18,'18"'),
        (19,'19"'),
        (20,'20"'),
        (21,'21"'),
        (22,'22"'),
        (23,'23"'),
        (24,'24"'),
        (25,'25"'),
        (26,'26"'),
    )
    GROWTH_PATTERN_CHOICES = (
        ('Slow','Slow'),
        ('Moderate','Moderate'),
        ('Fast','Fast'),
    )
    PRUNING_CHOICES = (
        ('Every Month','Every Month'),
        ('1-2 Month','1-2 Month'),
        ('2-3 Month','2-3 Month'),
        ('3-4 Month','3-4 Month'),
        ('4-5 Month','4-5 Month'),
        ('5-6 Month','5-6 Month'),
        ('6-7 Month','6-7 Month'),
        ('7-8 Month','7-8 Month'),
        ('8-9 Month','8-9 Month'),
        ('9-10 Month','9-10 Month'),
    )
    RE_POTTING_CHOICES = (
        ('Every 3-4 Month','Every 3-4 Month'),
        ('Every 5-6 Month','Every 5-6 Month'),
        ('Every 6-7 Month','Every 6-7 Month'),
        ('Every 7-8 Month','Every 7-8 Month'),
        ('Every 8-9 Month','Every 8-9 Month'),
        ('Every 9-10 Month','Every 9-10 Month'),
        ('Every 10-11 Month','Every 10-11 Month'),
        ('Every 11-12 Month','Every 11-12 Month'),
        ('Every 12-13 Month','Every 12-13 Month'),
        ('Every 13-14 Month','Every 13-14 Month'),
        ('Every 14-15 Month','Every 14-15 Month'),
        ('Every 15-16 Month','Every 15-16 Month'),
        ('Every 16-17 Month','Every 16-17 Month'),
        ('Every 17-18 Month','Every 17-18 Month'),
    )
    TOXICITY_CHOICES = (
        ('YES','YES'),
        ('NO','NO')
    )
    name = models.CharField(max_length=150,null= True, default=None)
    product_type = models.CharField(max_length=50,choices=PRODUCT_TYPE_CHOICES,default='Plants')
    actual_price=models.PositiveIntegerField(default=0)
    price_before_sale = models.PositiveIntegerField(null=True, blank=True)
    selling_price=models.PositiveIntegerField(default=0)
    nutritional_value = models.CharField(max_length=100,null = True,blank=True, default=None)
    category = models.ManyToManyField(Category)
    giftcategory = models.ForeignKey(GiftingCategory,default="")
    price_category = models.ForeignKey(PriceCategory)
    images = GenericRelation(Images)
    about = models.TextField(max_length=2500,null = True, default=None)

    how_to_grow_soil_need = models.CharField(max_length=250,null = True,blank=True, default=None)
    how_to_grow_fertilizer_type   = models.CharField(max_length=250,null = True,blank=True, default=None)

    how_to_grow_process = models.TextField(max_length=5000,null = True,blank=True, default = None)

    how_to_grow_growth_pattern   = models.CharField(max_length=50,choices=GROWTH_PATTERN_CHOICES,default='Slow')
    how_to_grow_pruning   = models.CharField(max_length=50,choices=PRUNING_CHOICES,default='Every Month')
    how_to_grow_re_potting   = models.CharField(max_length=50,choices=RE_POTTING_CHOICES,default='Every 3-4 Month')

    maintenance_tip_do = models.TextField(max_length=5000,null=True,blank=True,default=None)
    maintenance_tip_dont = models.TextField(max_length=5000,null=True,blank=True,default=None)
    # benefits = models.ManyToManyField(Benefit)
    benefits = models.TextField(max_length=1000,null=True,blank=True,default=None)
    placement = models.CharField(max_length=50,choices=CHOICE,default='Anywhere')
    tags = models.ManyToManyField(Tags)
    # pot_size_min = models.PositiveIntegerField(choices=POT_SIZE_CHOICES,default=4)
    # pot_size_max = models.PositiveIntegerField(choices=POT_SIZE_CHOICES,default=8)
    season = models.ManyToManyField(Season,blank=True,default=None)
    toxicity = models.CharField(max_length=100, choices=TOXICITY_CHOICES, null= True,blank=True,default='NO')
    maintenance_level = models.ForeignKey(MaintenanceLevel,null= True,blank=True,default=None)
    min_height = models.PositiveIntegerField(default=0)
    max_height = models.PositiveIntegerField(default=0)
    water_frequency_summer = models.CharField(max_length=150,choices=WATER,default = 'Daily')
    water_frequency_winter = models.CharField(max_length=150,choices=WATER,default = 'Daily')
    fertilizer_frequency_summer = models.CharField(max_length=150,choices=FERTILIZER,default = 'No')
    fertilizer_frequency_winter = models.CharField(max_length=150,choices=FERTILIZER,default = 'No')
    family_name = models.CharField(max_length=150,null=True,blank=True,default=None)
    synonyms = models.CharField(max_length=500,null=True,blank=True,default=None)
    fragrance = models.CharField(max_length=50,choices=FRAGRANCE,default='None')
    plant_type = models.CharField(max_length=50,choices=PLANT_TYPE_CHOICES,default = 'None')
    flower = models.BooleanField(default=False)
    flower_color = models.CharField(max_length=100,null = True,blank=True,default=None)
    oxygen_sunlight = models.BooleanField(default=False)
    oxygen_night = models.BooleanField(default=False)
    stock = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    width = models.PositiveIntegerField(null = True,blank=True,verbose_name='Width/Length',default=0)
    height = models.PositiveIntegerField(null = True,blank=True,default=0)
    diameter = models.PositiveIntegerField(null = True,blank=True,default=0)
    shipping_info = models.TextField(max_length=4000,null=True,blank=True,default=None)
    title_tag = models.CharField(max_length=500,blank=True,null= True)
    meta_description = models.CharField(max_length=500,blank=True,null= True, default=None)
    meta_keyword = models.CharField(max_length=500,blank=True,null= True, default=None)
    product_sku = models.CharField(max_length=150,null=True,default=None,unique=True)
    slug = models.SlugField(max_length=200, null=True,blank=True,unique=True,default=None)
    custom_header_meta = models.CharField(max_length=2000,null= True,blank=True, default=None)
    custom_script_seo = models.CharField(max_length=2000,null= True,blank=True, default=None)

    @property
    def _season(self):
        se=[]
        for s in self.season.all():
            se.append(s.name)
        return se

    def is_active(self):
        return (self.active and self.selling_price>0 and self.stock)
        #  and self.stock
    @property
    def grade_list(self):
        d=[]
        for g in self.tags.all():
            d.append(g.name)
        return d
        # return "\n,".join([str(g.name) for g in self.tags.all()])
    @property
    def _category(self):
        cat = []
        for c in self.category.all():
            cat.append(c.name)
        return cat
    def __unicode__(self):
        return '{}'.format(self.name)

    def clean(self, *args, **kwargs):
        if self.price_before_sale is not None and self.price_before_sale <= self.selling_price:
            raise ValidationError('Selling price can not be greater than price before selling.')
        super(Plants, self).clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.full_clean()
        s = slugify(self.name)
        if self.slug==None:
            self.slug = 'buy-'+s+'-'+self.product_type+'-online-in-delhi'
        super(Plants, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Plant'
        verbose_name_plural = 'Plants'
        ordering = ['-id']

    @property
    def my_image(self):
        try:
            image = {'image':self.images.all()[0].image,'alt':self.images.all()[0].alt,'title':self.images.all()[0].title}
            return image
        except:
            return {'image':'','alt':'','title':''}

class UserProfile(Base):
    """docstring for UserProfile."""
    CHOICE=(
        ('vendor','Vendor'),
        ('delivery_boy','Delivery Boy'),
        ('customer','Customer')
    )
    userType=models.CharField(max_length=50,choices=CHOICE,default='customer')
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=10,blank=True,null=True,unique=True)
    date_of_birth=models.DateField(null=True,blank=True)
    name=models.CharField(max_length=200,null=True,blank=True,default='')

    address_line1 = models.CharField(max_length=250,null=True,blank=True,default = '')
    address_line2 = models.CharField(max_length=250,null=True,blank=True,default = '')
    state = models.CharField(max_length=100,null  = True,blank = True,default = '')
    city = models.CharField(max_length=100,null = True,blank = True,default = '')
    nearest_landmark = models.CharField(max_length=250,null = True,blank = True,default = '')
    pincode = models.PositiveIntegerField(blank=True,null=True,default=None)
    forgot_code = models.CharField(max_length=50, blank=True, null=True)

    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)

    def __unicode__(self):
        return '{}'.format(self.user.username)

class PlantStock(Base):
    """docstring for PlantStock."""
    plant = models.ForeignKey(Plants)
    price = models.PositiveIntegerField(default = 1)
    user = models.ForeignKey(User)
    quantity = models.PositiveIntegerField(default = 0)
    def __unicode__(self):
        return '{}'.format(self.plant.name)


class Carts(Base):
    """docstring for Carts"""
    user = models.ForeignKey(User,null=True,default=None,on_delete=models.SET_NULL)
    name=models.CharField(max_length=200,null=True,blank=True)
    def __unicode__(self):
        return '{}'.format(self.user)
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

class CartItem(Base):
    """docstring for CartItem."""
    plant = models.ForeignKey(Plants)
    cart = models.ForeignKey(Carts)
    quantity = models.PositiveIntegerField(default = 1)
    price = models.PositiveIntegerField(default = 1)
    def __unicode__(self):
        return '{}'.format(self.cart.name)
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

DELIVERY_TIME = (
    ('10am_12pm','10:00 am - 12:00 pm'),
    ('12pm_02pm','12:00 pm - 02:00 pm'),
    ('02pm_04pm','02:00 pm - 04:00 pm'),
    ('04pm_06pm','04:00 pm - 06:00 pm')
)
STATUS_CHOICE = (
    ('payment_not_done','PAYMENT NOT DONE'),
    ('payment_done','PAYMENT DONE'),
    ('order_placed','ORDER PLACED'),
    ('pending_customer_approval','PAINDING CUSTOMER APPROVAL'),
    ('customer_approval_done','CUSTOMER_APPROVAL_DONE'),
    ('in_process','IN PROCESS'),
    ('dispatched','Dispatched'),
    ('canceled','Canceled'),
    ('delivered','DELIVERED'),

)

class  Booking(Base):
    """docstring for Booking."""
    PAYMENT_TYPE=(
        ('online_payu','ONLINE PAYUMONEY'),
        ('on_cash','ON CASH')
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    status=models.CharField(max_length=50,choices=STATUS_CHOICE, default='payment_not_done')
    payment_type = models.CharField(max_length=150,choices=PAYMENT_TYPE, default='on_cash')
    plant_details=JSONField()
    amount=models.PositiveIntegerField(default=0)
    coupon_discount = models.PositiveIntegerField(default=0)
    coupon = models.ForeignKey(Coupon,blank=True,null=True,default=None,on_delete=models.SET_NULL)
    placed_on = models.DateTimeField(default=datetime.now)
    shipping_name = models.CharField(max_length=150,null=True)
    shipping_phone = models.CharField(max_length=150,null=True)
    shipping_email = models.CharField(max_length=150,null=True, blank=True)
    shipping_address1 = models.CharField(max_length=150,null=True)
    shipping_address2 = models.CharField(max_length=150,null=True)
    shipping_city = models.CharField(max_length=150,null=True)
    shipping_pincode = models.CharField(max_length=150,null=True)
    shipping_state = models.CharField(max_length=150,null=True)
    is_gift = models.BooleanField(default=False)
    gift_text = models.CharField(max_length=150,null=True,blank=True,default = None)
    delivery_date = models.DateField(default=datetime.today())
    delivery_time = models.CharField(max_length=150,choices=DELIVERY_TIME, default='10am_12pm')
    shipping_latitude = models.FloatField(default=0.0)
    shipping_longitude = models.FloatField(default=0.0)
    delivery_charge=models.PositiveIntegerField(default=0)
    def __unicode__(self):
        order_id = "SO%(name)s%(date)s"%{"name":self.id,'date':date.today()}
        print("ORDER ID --------------->",order_id)
        print("Booking ID ------------------->",order_id)
        return '{}'.format(order_id)
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Booking'


class  DeliveryBoyOrder(Base):
    """
    Function for bifurcate order to delivery boy.
    """
    delivery_boy = models.ForeignKey(User,blank=True,null=True,default=None,on_delete=models.SET_NULL)   # assign by admin
    order =  models.OneToOneField(Booking,on_delete=models.CASCADE)
    def __unicode__(self):
        return u'%s order id %s' % (self.order.user.username, self.order.id)
    class Meta:
        verbose_name = 'Delivery Boy Order'
        verbose_name_plural = 'Delivery Boy Order'

RATING_CHOICE=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
REVIEW_STATUS_CHOICE = (
    ('pending', 'Pending'),
    ('approved', 'Approved')
)
class Review(Base):
    """
    Function for review plants.
    """
    review = models.TextField(max_length=500,null=True,default = None)
    rating =  models.PositiveIntegerField(choices=RATING_CHOICE, default=5)
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    plant = models.ForeignKey(Plants,null=True,on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, null=True, choices=REVIEW_STATUS_CHOICE, default='pending')
    def __unicode__(self):
        return u'%s review %s' % (self.plant, self.user)
    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Review'



class OrderDetails(Base):
    """
    Function for bifurcate booking details.
    """
    vendor = models.ForeignKey(User,blank=True,null=True,default=None,on_delete=models.SET_NULL)   # assign by admin
    order =  models.ForeignKey(Booking,on_delete=models.CASCADE)
    
    plant = models.ForeignKey(Plants)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50,choices=STATUS_CHOICE, default='in_process')
    vendor_ids = models.CharField(max_length=500,blank=True,null=True,default='')
    images = GenericRelation(Images)
    def __unicode__(self):
        return u'%s order id %s' % (self.order.user.username,self.order.id)
    class Meta:
        verbose_name = 'Order Detail'
        verbose_name_plural = 'Order Details'





class PaymentTransaction(Base):
    """docstring for PaymentTransaction."""
    CHOICE=(
        ('not_initiated','NOT_INITIATED'),
        ('success','SUCCESS'),
        ('failure','FAILURE'),
        ('cancelled','CANCELLED')
    )
    def transaction_default():
        """return default dict for the booking_details field"""
        return {}
    booking = models.ForeignKey(Booking)
    invoice_id=models.CharField(max_length=25,default='')
    status=models.CharField(max_length=50,choices=CHOICE,default='not_initiated')
    payee_name = models.CharField(max_length=150,null=True)
    payee_mobile=models.CharField(max_length=150,blank=True,null=True)
    payee_email=models.CharField(max_length=150)
    amount=models.PositiveIntegerField(default=0)
    returned_details=JSONField(default=transaction_default())


class PlantQuestionAnswer(Base):
    """docstring for State list model"""
    question = models.CharField(max_length=350,null=True)
    answer = models.TextField(max_length=1000,null= True)
    plant = models.ForeignKey(Plants)
    def __unicode__(self):
        return '{}'.format(self.question)
    class Meta:
        verbose_name = 'Plant Question Answer'
        verbose_name_plural = 'Plant Question Answer'




class State(Base):
    """docstring for State list model"""
    name = models.CharField(max_length=150,blank=True,null=True)
    code = models.CharField(max_length=20,blank=True,null=True)
    def __unicode__(self):
        return '{}'.format(self.name)
    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'


class Cities(Base):
    """docstring for City list model"""
    name = models.CharField(max_length=250,blank=True,null=True)
    state = models.ForeignKey(State)
    def __unicode__(self):
        return '{}'.format(self.name)
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class Testimonials(Base):
    """
    docstring for Testimonial model
    """
    name = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='images/')
    designation = models.CharField(max_length=100,null=True,blank=True)
    text = models.TextField(max_length=300,null=True)
    def __unicode__(self):
        return u'%s %s' % (self.name, self.designation)
    class Meta:
        verbose_name = 'Testimonial'
        verbose_name_plural = 'Testimonials'


class DeliveryChargeConfig(Base):
    """
    Model for config delivery charges
    """
    max_amount = models.PositiveIntegerField(verbose_name='Maximum amount for delivery charge')
    delivery_charge = models.PositiveIntegerField()
    def __unicode__(self):
        return u'Rs %s delivery charge apply if booking amount less than Rs %s' % (self.delivery_charge, self.max_amount)
    class Meta:
        verbose_name = 'Config Delivery Charge'
        verbose_name_plural = 'Config Delivery Charge'

    # validators=[MinValueValidator(20),MaxValueValidator(150)]

class CorporateGift(Base):
    """
    Model for store corporate gifting
    """
    title = models.CharField(max_length=250,null=True)
    image = models.ImageField(upload_to='images/')
    def __unicode__(self):
        return u'%s' % (self.title)
    def image_tag(self):
        return u'<a href="%s" data_target="_blank"><img src="%s" alt="No Image" height="50" width="50" /></a>' % (self.image.url,self.image.url)
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True
    class Meta:
        verbose_name = 'Corporate Gift'
        verbose_name_plural = 'Corporate Gift'


class OnlineNersery(Base):
    """
    Model for store Online Nersery
    """
    page_title = models.CharField(max_length=250,null=True)
    banner_image = models.ImageField(upload_to='images/')
    categories = models.ManyToManyField('Category',verbose_name='Select Category')
    meta_title = models.CharField(max_length=250,null=True)
    meta_description = models.CharField(max_length=500,blank=True,null= True)
    meta_keyword = models.CharField(max_length=500,blank=True,null= True)
    long_content = models.TextField(max_length=25000,blank=True,null= True)
    def __unicode__(self):
        return u'%s' % (self.page_title)
    class Meta:
        verbose_name = 'Online Nursery'
        verbose_name_plural = 'Online Nursery'

class OnlineNerseryCategory(Base):
    """
    Model for store Online Nersery
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    online_nersery = models.ForeignKey(OnlineNersery, on_delete=models.CASCADE)
    plants = models.ManyToManyField(Plants,verbose_name='Select Plants')
    def __unicode__(self):
        return u'%s' % (self.category)
    class Meta:
        verbose_name = 'Online Nursery Category'
        verbose_name_plural = 'Online Category'

class DiwaliGifts(Base):
    """
    diwali page plants
    """
    title = models.CharField(max_length=500,blank=True,null= True)
    description = models.CharField(max_length=500,blank=True,null= True, default=None)
    keyword = models.CharField(max_length=500,blank=True,null= True, default=None)
    plants = models.ManyToManyField(Plants,verbose_name='Select Plants')
    def __unicode__(self):
        return u'%s' % (self.title)
    class Meta:
        verbose_name = 'Diwali Gifts Page'
        verbose_name_plural = 'Diwali Gifts Page'


class CategoryPagePromotionalBanner(Base):
    """
    Model for store Online Nersery
    """
    banner_image = models.ImageField(upload_to='images/')
    banner_title = models.CharField(max_length=350,null=True)
    link = models.CharField(max_length=350,null=True)
    def __unicode__(self):
        return u'%s' % (self.banner_title)
    class Meta:
        verbose_name = 'Category page promotional banner'
        verbose_name_plural = 'Category page promotional banner'

class OfferSlider(Base):
    """
    model to store offer slider
    """
    heading = models.CharField(max_length=100,null=True)
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=350,null=True)
    link = models.CharField(max_length=350,null=True)
    link_text = models.CharField(max_length=350,null=True)
    created_at = models.DateTimeField(default=datetime.now,editable=False)
    def __unicode__(self):
        return u'%s' % (self.title)
    class Meta:
        verbose_name = 'Offer Slider'
        verbose_name_plural = 'Offer Slider'




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        name = instance.first_name+' '+instance.last_name
        UserProfile.objects.create(user=instance,name=name)
    # instance.userprofile.save()





######################## NEW MODEL ADDED########################
# class Gifting(Base):
#     """docstring for Category"""
#     TYPE_CHOICES = (
#         ('Plants','Plants'),
#         ('Accessories','Accessories'),
#         ('Gifting','Gifting')
#     )
#     name = models.CharField(max_length=150,null= True, default=None)
#     slug = models.SlugField(max_length=200, null=True,blank=True,unique=True,default=None)
#     banner_images = GenericRelation(Images)
#     banner_text = models.TextField(max_length=500,null= True, default=None)
#     feature_text = models.TextField(max_length=500,null= True, default=None)
#     thumbnail = models.ImageField(upload_to='images/',default='images/product-image.jpg')
#     description = models.TextField(max_length=1000,null= True, default=None)
#     parent_category = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE)
#     benefits = models.ManyToManyField(Benefit)
#     synonyms = models.CharField(max_length=250,null=True,blank=True,default=None)
#     title_tag = models.CharField(max_length=500,blank=True,null= True)
#     meta_description = models.CharField(max_length=500,blank=True,null= True, default=None)
#     meta_keyword = models.CharField(max_length=500,blank=True,null= True, default=None)
#     long_contents = models.TextField(max_length=25000,blank=True,null= True, default=None)
#     video_url = models.URLField(max_length=500,null=True,default=None)
#     category_type = models.CharField(max_length=50,choices=TYPE_CHOICES,default='Plants')
#     custom_header_meta = models.CharField(max_length=2000,null= True, blank=True, default=None)
#     custom_script_seo = models.CharField(max_length=2000,null= True, blank=True, default=None)

#     def __unicode__(self):
#         return '{}'.format(self.name)
#     def save(self, *args, **kwargs):
#         s = slugify(self.name)
#         if self.slug==None or self.slug=='':
#             self.slug = 'buy-'+s+'-online-in-delhi'
#         super(Gifting, self).save(*args, **kwargs)

#     class Meta:
#         verbose_name = 'Gifting'
#         verbose_name_plural = 'Giftings'


# class GiftingCategory(Base):
#     gifting_type = models.ForeignKey(Gifting,on_delete=models.CASCADE)
#     parent_category = models.ForeignKey('self',blank=True,null=True,on_delete=models.CASCADE)
#     name = models.CharField(max_length=500)
#     slug = models.SlugField(max_length=200, null=True,blank=True,unique=True,default=None)
#     description = models.TextField(max_length=1000,null= True, default=None)
#     thumbnail = models.ImageField(upload_to='images/',default='images/product-image.jpg')

#     def __unicode__(self):
#         return '{}'.format(self.name)

#     class Meta:
#         verbose_name = 'GiftingCategory'
#         verbose_name_plural = 'GiftingCategories'





# class GiftingCategoryProduct(Base):
#     """docstring for Plants."""
#     CHOICE=(
#         ('Outdoor-Sunny','Outdoor-Sunny'),
#         ('Outdoor-Shades','Outdoor-Shades'),
#         ('Indoor','Indoor'),
#         ('Outdoor-Sunny or Indoor','Outdoor-Sunny or Indoor'),
#         ('Outdoor-Shades or Indoor','Outdoor-Shades or Indoor'),
#         ('Anywhere','Anywhere')
#     )
#     FRAGRANCE = (
#         ('Strong','Strong'),
#         ('Low','Low'),
#         ('Medium','Medium'),
#         ('None','None')
#     )
#     WATER = (
#         ('Alternate Day','Alternate Day'),
#         ('Daily','Daily'),
#         ('Twice Week','Twice Week'),
#         ('Weekly','Weekly'),
#         ('Monthly','Monthly'),
#     )
#     FERTILIZER = (
#         ('Every Month','Every Month'),
#         ('1-2 Month','1-2 Month'),
#         ('2-3 Month','2-3 Month'),
#         ('3-4 Month','3-4 Month'),
#         ('4-5 Month','4-5 Month'),
#         ('5-6 Month','5-6 Month'),
#         ('6-7 Month','6-7 Month'),
#         ('7-8 Month','7-8 Month'),
#         ('8-9 Month','8-9 Month'),
#         ('9-10 Month','9-10 Month'),
#         ('No','No'),
#     )
#     PLANT_TYPE_CHOICES = (
#         ('Fruit','Fruit'),
#         ('Vegetable','Vegetable'),
#         ('None','None'),
#     )
#     PRODUCT_TYPE_CHOICES = (
#         ('Plants','Plants'),
#         ('Seeds','Seeds'),
#         ('Pots','Pots'),
#         ('Tools','Tools'),
#         ('Fertilizers','Fertilizers'),
#         ('Soil','Soil'),
#         ('Combos','Combos'),
#         ('Organic Compose','Organic Compose'),
#     )
#     POT_SIZE_CHOICES = (
#         (4,'4"'),
#         (5,'5"'),
#         (6,'6"'),
#         (7,'7"'),
#         (8,'8"'),
#         (9,'9"'),
#         (10,'10"'),
#         (11,'11"'),
#         (12,'12"'),
#         (13,'13"'),
#         (14,'14"'),
#         (15,'15"'),
#         (16,'16"'),
#         (17,'17"'),
#         (18,'18"'),
#         (19,'19"'),
#         (20,'20"'),
#         (21,'21"'),
#         (22,'22"'),
#         (23,'23"'),
#         (24,'24"'),
#         (25,'25"'),
#         (26,'26"'),
#     )
#     GROWTH_PATTERN_CHOICES = (
#         ('Slow','Slow'),
#         ('Moderate','Moderate'),
#         ('Fast','Fast'),
#     )
#     PRUNING_CHOICES = (
#         ('Every Month','Every Month'),
#         ('1-2 Month','1-2 Month'),
#         ('2-3 Month','2-3 Month'),
#         ('3-4 Month','3-4 Month'),
#         ('4-5 Month','4-5 Month'),
#         ('5-6 Month','5-6 Month'),
#         ('6-7 Month','6-7 Month'),
#         ('7-8 Month','7-8 Month'),
#         ('8-9 Month','8-9 Month'),
#         ('9-10 Month','9-10 Month'),
#     )
#     RE_POTTING_CHOICES = (
#         ('Every 3-4 Month','Every 3-4 Month'),
#         ('Every 5-6 Month','Every 5-6 Month'),
#         ('Every 6-7 Month','Every 6-7 Month'),
#         ('Every 7-8 Month','Every 7-8 Month'),
#         ('Every 8-9 Month','Every 8-9 Month'),
#         ('Every 9-10 Month','Every 9-10 Month'),
#         ('Every 10-11 Month','Every 10-11 Month'),
#         ('Every 11-12 Month','Every 11-12 Month'),
#         ('Every 12-13 Month','Every 12-13 Month'),
#         ('Every 13-14 Month','Every 13-14 Month'),
#         ('Every 14-15 Month','Every 14-15 Month'),
#         ('Every 15-16 Month','Every 15-16 Month'),
#         ('Every 16-17 Month','Every 16-17 Month'),
#         ('Every 17-18 Month','Every 17-18 Month'),
#     )
#     TOXICITY_CHOICES = (
#         ('YES','YES'),
#         ('NO','NO')
#     )
#     giftcategory = models.ForeignKey(GiftingCategory,on_delete=models.CASCADE)
#     name = models.CharField(max_length=150,null= True, default=None)
#     product_type = models.CharField(max_length=50,choices=PRODUCT_TYPE_CHOICES,default='Plants')
#     actual_price=models.PositiveIntegerField(default=0)
#     price_before_sale = models.PositiveIntegerField(null=True, blank=True)
#     selling_price=models.PositiveIntegerField(default=0)
#     nutritional_value = models.CharField(max_length=100,null = True,blank=True, default=None)
#     category = models.ManyToManyField(Category)
#     price_category = models.ForeignKey(PriceCategory)
#     images = GenericRelation(Images)
#     about = models.TextField(max_length=2500,null = True, default=None)

#     how_to_grow_soil_need = models.CharField(max_length=250,null = True,blank=True, default=None)
#     how_to_grow_fertilizer_type   = models.CharField(max_length=250,null = True,blank=True, default=None)

#     how_to_grow_process = models.TextField(max_length=5000,null = True,blank=True, default = None)

#     how_to_grow_growth_pattern   = models.CharField(max_length=50,choices=GROWTH_PATTERN_CHOICES,default='Slow')
#     how_to_grow_pruning   = models.CharField(max_length=50,choices=PRUNING_CHOICES,default='Every Month')
#     how_to_grow_re_potting   = models.CharField(max_length=50,choices=RE_POTTING_CHOICES,default='Every 3-4 Month')

#     maintenance_tip_do = models.TextField(max_length=5000,null=True,blank=True,default=None)
#     maintenance_tip_dont = models.TextField(max_length=5000,null=True,blank=True,default=None)
#     # benefits = models.ManyToManyField(Benefit)
#     benefits = models.TextField(max_length=1000,null=True,blank=True,default=None)
#     placement = models.CharField(max_length=50,choices=CHOICE,default='Anywhere')
#     tags = models.ManyToManyField(Tags)
#     # pot_size_min = models.PositiveIntegerField(choices=POT_SIZE_CHOICES,default=4)
#     # pot_size_max = models.PositiveIntegerField(choices=POT_SIZE_CHOICES,default=8)
#     season = models.ManyToManyField(Season,blank=True,default=None)
#     toxicity = models.CharField(max_length=100, choices=TOXICITY_CHOICES, null= True,blank=True,default='NO')
#     maintenance_level = models.ForeignKey(MaintenanceLevel,null= True,blank=True,default=None)
#     min_height = models.PositiveIntegerField(default=0)
#     max_height = models.PositiveIntegerField(default=0)
#     water_frequency_summer = models.CharField(max_length=150,choices=WATER,default = 'Daily')
#     water_frequency_winter = models.CharField(max_length=150,choices=WATER,default = 'Daily')
#     fertilizer_frequency_summer = models.CharField(max_length=150,choices=FERTILIZER,default = 'No')
#     fertilizer_frequency_winter = models.CharField(max_length=150,choices=FERTILIZER,default = 'No')
#     family_name = models.CharField(max_length=150,null=True,blank=True,default=None)
#     synonyms = models.CharField(max_length=500,null=True,blank=True,default=None)
#     fragrance = models.CharField(max_length=50,choices=FRAGRANCE,default='None')
#     plant_type = models.CharField(max_length=50,choices=PLANT_TYPE_CHOICES,default = 'None')
#     flower = models.BooleanField(default=False)
#     flower_color = models.CharField(max_length=100,null = True,blank=True,default=None)
#     oxygen_sunlight = models.BooleanField(default=False)
#     oxygen_night = models.BooleanField(default=False)
#     stock = models.BooleanField(default=False)
#     active = models.BooleanField(default=True)
#     featured = models.BooleanField(default=False)
#     width = models.PositiveIntegerField(null = True,blank=True,verbose_name='Width/Length',default=0)
#     height = models.PositiveIntegerField(null = True,blank=True,default=0)
#     diameter = models.PositiveIntegerField(null = True,blank=True,default=0)
#     shipping_info = models.TextField(max_length=4000,null=True,blank=True,default=None)
#     title_tag = models.CharField(max_length=500,blank=True,null= True)
#     meta_description = models.CharField(max_length=500,blank=True,null= True, default=None)
#     meta_keyword = models.CharField(max_length=500,blank=True,null= True, default=None)
#     product_sku = models.CharField(max_length=150,null=True,default=None,unique=True)
#     slug = models.SlugField(max_length=200, null=True,blank=True,unique=True,default=None)
#     custom_header_meta = models.CharField(max_length=2000,null= True,blank=True, default=None)
#     custom_script_seo = models.CharField(max_length=2000,null= True,blank=True, default=None)

#     @property
#     def _season(self):
#         se=[]
#         for s in self.season.all():
#             se.append(s.name)
#         return se

#     def is_active(self):
#         return (self.active and self.selling_price>0 and self.stock)
#         #  and self.stock
#     @property
#     def grade_list(self):
#         d=[]
#         for g in self.tags.all():
#             d.append(g.name)
#         return d
#         # return "\n,".join([str(g.name) for g in self.tags.all()])
#     @property
#     def _category(self):
#         cat = []
#         for c in self.category.all():
#             cat.append(c.name)
#         return cat
#     def __unicode__(self):
#         return '{}'.format(self.name)

#     def clean(self, *args, **kwargs):
#         if self.price_before_sale is not None and self.price_before_sale <= self.selling_price:
#             raise ValidationError('Selling price can not be greater than price before selling.')
#         super(GiftingCategoryProduct, self).clean(*args, **kwargs)

#     def save(self, *args, **kwargs):
#         self.full_clean()
#         s = slugify(self.name)
#         if self.slug==None:
#             self.slug = 'buy-'+s+'-'+self.product_type+'-online-in-delhi'
#         super(GiftingCategoryProduct, self).save(*args, **kwargs)

#     class Meta:
#         verbose_name = 'GiftingCategoryProduct'
#         verbose_name_plural = 'GiftingCategoryProduct'
#         ordering = ['-id']

#     @property
#     def my_image(self):
#         try:
#             image = {'image':self.images.all()[0].image,'alt':self.images.all()[0].alt,'title':self.images.all()[0].title}
#             return image
#         except:
#             return {'image':'','alt':'','title':''}





# class GiftingQuestionAnswer(Base):
#     """docstring for State list model"""
#     question = models.CharField(max_length=350,null=True)
#     answer = models.TextField(max_length=1000,null= True)
#     gifting = models.ForeignKey(GiftingCategoryProduct)
#     def __unicode__(self):
#         return '{}'.format(self.question)
#     class Meta:
#         verbose_name = 'Gifting Question Answer'
#         verbose_name_plural = 'Gifting Question Answer'
