from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User,Group
from .models import *
from web.forms import *
from core.utils import *
from django.contrib.contenttypes.admin import GenericTabularInline
from import_export import resources
from import_export.admin import ImportExportModelAdmin,ImportMixin,ExportMixin,ImportExportMixin
from import_export import fields
import json
from django.db.models import Q
# Register your models here.
class ImagesInline(GenericTabularInline):
    model = Images
    extra = 1
    min_num = 0
    max_num = 8
    ct_field_name = 'content_type'
    id_field_name = 'object_id'

class PlantResource(resources.ModelResource):
    class Meta:
        model = Plants
class UserResource(resources.ModelResource):
    name = fields.Field(column_name='name')
    mobile = fields.Field(column_name='mobile')
    order_amount = fields.Field(column_name='order amount')
    plant_name = fields.Field(column_name='plant name')
    class Meta:
        model = User
        exclude = ('password','user_permissions','last_login','is_superuser','groups','user_permission','first_name','last_name','is_staff',)
        export_order = ('id','username','name','mobile','email','is_active','date_joined')
    def dehydrate_name(self, user):
        try:
            return user.userprofile.name
        except:
            return ''
    def dehydrate_mobile(self, user):
        try:
            return user.userprofile.mobile
        except:
            return ''
    def dehydrate_order_amount(self, user):
        from django.db.models import Sum
        try:
            return Booking.objects.filter(~Q(status = 'payment_not_done') and Q(user=user)).aggregate(tot=Sum('amount'))['tot']
        except:
            return 0

    def dehydrate_plant_name(self, user):
        plants = []
        try:
            booking = Booking.objects.filter(~Q(status = 'payment_not_done') and Q(user=user))
            for b in booking:
                plant = json.loads(b.plant_details)
                for p in plant:
                    plants.append(p['plant']['name'])
            used = set()
            pl = [x for x in plants if x not in used and (used.add(x) or True)]
            return ','.join(pl)
        except:
            return ''

class DeliveryBoyOrderInline(admin.StackedInline):
    model = DeliveryBoyOrder
    can_delete = False
    fk_name = 'order'
    form = DeliveryBoyOrderForm


class CategoryInline(ExportMixin,admin.ModelAdmin):
    model = Category
    inlines = (ImagesInline,)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','parent_category')
    search_fields = ('name','parent_category__name','benefits__title')
    class Media:
        js = (
            '/static/tiny_mce/tiny_mce.js',
            '/static/textarea.js'
        )


################# NEW Gifting Admin Class Added#####################
# class GiftingInline(ExportMixin,admin.ModelAdmin):
#     model = Gifting
#     inlines = (ImagesInline,)
#     prepopulated_fields = {"slug": ("name",)}
#     list_display = ('name','parent_category')
#     search_fields = ('name','parent_category__name','benefits__title')
#     class Media:
#         js = (
#             '/static/tiny_mce/tiny_mce.js',
#             '/static/textarea.js'
#         )



class GiftingCategoryInline(ExportMixin,admin.ModelAdmin):
    model = GiftingCategory
    inlines = (ImagesInline,)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','gifting_type')
    search_fields = ('name','gifting_type__name')
    class Media:
        js = (
            '/static/tiny_mce/tiny_mce.js',
            '/static/textarea.js'
        )



# class GiftingCategoryProductInline(ImportExportMixin, admin.ModelAdmin):
#     model = GiftingCategoryProduct
#     form = PlantsFieldForm
#     resource_class = PlantResource
#     inlines = (ImagesInline,)
#     prepopulated_fields = {"slug": ("name",)}
#     list_display = ('name','product_type','actual_price','selling_price','stock','active')
#     list_filter = ['category','stock','active']
#     search_fields = ('name','product_type')
#     class Media:
#         js = (
#             '/static/tiny_mce/tiny_mce.js',
#             '/static/textarea.js'
#         )



class TagsAdmin(ExportMixin,admin.ModelAdmin):
    pass

class PriceCategoryAdmin(ExportMixin,admin.ModelAdmin):
    pass

class MaintenanceLevelAdmin(ExportMixin,admin.ModelAdmin):
    pass

class SeasonAdmin(ExportMixin,admin.ModelAdmin):
    pass


class PlantInline(ImportExportMixin, admin.ModelAdmin):
    model = Plants
    form = PlantsFieldForm
    resource_class = PlantResource
    inlines = (ImagesInline,)
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name','product_type','actual_price','selling_price','stock','active')
    list_filter = ['category','stock','active']
    search_fields = ('name','product_type')
    class Media:
        js = (
            '/static/tiny_mce/tiny_mce.js',
            '/static/textarea.js'
        )

class QuestionAnswerInline(admin.ModelAdmin):
    """Add text editor"""
    model = PlantQuestionAnswer
    list_display = ('question','plant_name')
    search_fields = ('question','plant__name')
    def plant_name(self,obj):
        return obj.plant.name

    class Media:
        js = (
            '/static/tiny_mce/tiny_mce.js',
            '/static/textarea.js'
        )



# class ProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False
#     verbose_name_plural = 'Profile'
#     fk_name = 'user'
#
class CustomUserAdmin(ExportMixin,UserAdmin):
    resource_class = UserResource
    list_display = ('username', 'email', 'first_name', 'is_staff','is_active')

class UserProfileAdmin(admin.ModelAdmin):
    """
    User Profile Admin view
    """
    list_display = ('get_username', 'get_email','userType','mobile','date_of_birth')
    search_fields = ('user__username', 'name','userType')
    def get_username(self, instance):
        return instance.user.username
    get_username.short_description = 'User Name'
    def get_email(self, instance):
        return instance.user.email
    get_email.short_description = 'Email'


class BookingAdmin(admin.ModelAdmin):
    """Booking Admin"""
    list_display = ('customer','id','get_quantity','status','payment_type','amount','placed_on','delivery_date','delivery_time','is_gift','get_invoice')
    list_filter = ['status', 'is_gift','delivery_time']
    search_fields = ('user__username', 'status','placed_on')
    readonly_fields = ['user','coupon','plant_details']
    inlines = (DeliveryBoyOrderInline, )
    def get_invoice(self, obj):
        return '<a target="_balnk" href="/admin/booking/%s/invoice">Invoice</a>' % ( obj.id)
    get_invoice.allow_tags = True
    get_invoice.short_description = 'Action'
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(BookingAdmin, self).get_inline_instances(request, obj)


    # actions = None
    # def has_delete_permission(self, request, obj=None):
    #     return False
    def has_add_permission(self, request):
        return False
    def customer(self, obj):
        return obj.user
    def get_quantity(self, obj):
        return OrderDetails.objects.filter(order=obj).count()
    get_quantity.short_description = 'No of Item'
    def save_model(self, request, obj, form, change):
        bk= Booking.objects.get(id=obj.id)
        s = form.cleaned_data['status']
        if bk.status != s:
            trigger_mail(s,bk)
        super(BookingAdmin, self).save_model(request, obj, form, change)


class OrderDetailsAdmin(admin.ModelAdmin):
    """
    function for OrderDetailsAdmin
    """
    list_display = ('order','plant','quantity','vendor','customer')
    readonly_fields = ['order','plant','customer','quantity']
    search_fields = ('order__id','plant__name')
    def customer(self, obj):
        return obj.order.user.username if obj.order.user else obj.order.shipping_phone
    def render_change_form(self,request, context, *args, **kwargs):
        obj = kwargs.pop("obj")
        v_ids = '6,4'
        v_ids = v_ids.split(',')
        # userprofile__id__in=v_ids
        if obj.vendor_ids =='':
            print obj.order
        context['adminform'].form.fields['vendor'].queryset = User.objects.filter(userprofile__userType='vendor')
        return super(OrderDetailsAdmin, self).render_change_form(request, context, args, kwargs)
    def has_add_permission(self, request):
        return False
    def save_model(self, request, obj, form, change):
        od= OrderDetails.objects.get(id=obj.id)
        v = form.cleaned_data['vendor']
        try:
            if od.vendor != v:
                html_content = '<p>Hi '+obj.vendor.username+'.</p><p>New Order for Product '+ obj.plant.name +' arrived. Order Id '+ str(obj.order.id) +'</p><p>Quantity: '+ str(obj.quantity) +'</p>'
                send_email(subject='Order Arrived',msg_body=html_content,emails=obj.vendor.email)
                m = 'new order arrived for product: '+obj.plant.name+' order id '+str(obj.order.id)+''
                send_message(mobiles=obj.vendor.username,message=m)
        except:
            pass
        super(OrderDetailsAdmin, self).save_model(request, obj, form, change)

class DeliveryChargeConfigAdmin(admin.ModelAdmin):
    """
    class for configure delivery charge admin
    """
    actions = None
    def has_add_permission(self, request):
        return False
    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False
    def save_model(self, request, obj, form, change):
        super(DeliveryChargeConfigAdmin, self).save_model(request, obj, form, change)
class CorporateGiftAdmin(admin.ModelAdmin):
    list_display = ('title','image_tag')
    search_fields = ('title',)


class PlantStockAdmin(ExportMixin, admin.ModelAdmin):
    model = PlantStock
    form = PlantsStockFieldForm
    list_display = ('get_plant_name','quantity','user')
    search_fields = ('plant__name','user__username')
    def get_plant_name(self,obj):
        return obj.plant.name
    get_plant_name.short_description = "Plant Name"

class OnlineNerseryCategoryInline(admin.StackedInline):
    model = OnlineNerseryCategory
    fk_name = 'online_nersery'
    extra = 0
    form = OnlineNerseryCategoryForm

class OnlineNerseryAdmin(admin.ModelAdmin):
    """
    OnlineNersery Admin Class
    """
    model = OnlineNersery
    inlines = [OnlineNerseryCategoryInline,]
    list_display = ('page_title',)
    filter_horizontal = ('categories',)

    class Media:
        js = (
            '/static/custom_online_nersery.js',
        )

class DiwaliGiftsAdmin(admin.ModelAdmin):
    list_display = ('title','description')
    filter_horizontal = ('plants',)


admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Benefit)
admin.site.register(Tags,TagsAdmin)
admin.site.register(Season,SeasonAdmin)
admin.site.register(Review)
admin.site.register(MaintenanceLevel,MaintenanceLevelAdmin)
admin.site.register(PriceCategory,PriceCategoryAdmin)
admin.site.register(Category,CategoryInline)
# admin.site.register(Gifting,GiftingInline)
admin.site.register(GiftingCategory,GiftingCategoryInline)
# admin.site.register(GiftingCategoryProduct,GiftingCategoryProductInline)
admin.site.register(Plants,PlantInline)
admin.site.register(OrderDetails,OrderDetailsAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(Booking,BookingAdmin)
admin.site.register(PlantQuestionAnswer,QuestionAnswerInline)
admin.site.register(Testimonials)
admin.site.register(DeliveryChargeConfig,DeliveryChargeConfigAdmin)
admin.site.register(PlantStock,PlantStockAdmin)
admin.site.register(CorporateGift,CorporateGiftAdmin)
admin.site.register(OnlineNersery,OnlineNerseryAdmin)
admin.site.register(CategoryPagePromotionalBanner)
admin.site.register(OfferSlider)
admin.site.register(DiwaliGifts,DiwaliGiftsAdmin)
