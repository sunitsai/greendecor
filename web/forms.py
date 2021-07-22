# @Author: Javed Ahamad
# @Date:   2017-02-16
# @Email:  javedahamad4@gmail.com
# @Filename: web/forms.py


from django import forms
from core.models import *
from django.db.models import Q

# def validate_mobile_number(self,mobile):
#         """"""
#         if not len(str(mobile))==10:
#             return True
#         return False

class RegistrationForm(forms.Form):
    """form for ther user registration"""
    email=forms.CharField(label="Email",max_length=254,widget=forms.EmailInput(attrs={'placeholder':"Enter a Valid email ID","class":"validation"}))
    username=forms.CharField(label="UserMobile",max_length=254,widget=forms.TextInput(attrs={'placeholder':"Enter 10 Digit Mobile Number","class":"validation"}))
    password=forms.CharField(label="Password",widget=forms.PasswordInput(attrs={"placeholder":"Set a Password for your Account","class":"validation"},render_value=True),)

    # def clean(self, *args, **kwargs):
    #     """
    #     Clean function
    #     """
    #     cleaned_data = super(RegistrationForm, self).clean()
    #     if validate_mobile_number(self,cleaned_data.get('username')):
    #         raise forms.ValidationError('Invalid mobile number, it must consist of 10 digits')
    #     else:
    #         return cleaned_data


class ShippingForm(forms.Form):
    """form for ther user registration"""
    shipping_name=forms.CharField(label="Name",max_length=150,widget=forms.TextInput(attrs={'placeholder':"Name","class":"input validation"}))
    shipping_phone=forms.CharField(label="Phone",max_length=150,widget=forms.NumberInput(attrs={'placeholder':"Phone","class":"input validation"}))
    shipping_email=forms.EmailField(label="Email",max_length=150,widget=forms.EmailInput(attrs={'placeholder':"Email","class":"input validation"}))
    shipping_address1=forms.CharField(label="Shipping Address 1",max_length=150,widget=forms.TextInput(attrs={"placeholder":"House / Flat Number","class":"input validation"}))
    shipping_address2=forms.CharField(label="Shipping Address 2",max_length=150,widget=forms.TextInput(attrs={"placeholder":"Enter Your Location Here...","class":"input validation"}))
    # shipping_city=forms.CharField(label="City",max_length=150,widget=forms.TextInput(attrs={"placeholder":"City","class":"input validation"}))
    shipping_city=forms.ChoiceField(label="City",widget=forms.Select(attrs={"placeholder":"Country","class":"input validation"}), choices=(('','Select City'),('Noida','Noida'),('Delhi','Delhi'),('New Delhi','New Delhi'),('Gurugram','Gurugram'),('Ghaziabad','Ghaziabad'),('Faridabad','Faridabad')))
    shipping_pincode=forms.CharField(label="Pincode",max_length=150,widget=forms.TextInput(attrs={"placeholder":"Pincode","class":"input validation"}))
    shipping_state=forms.CharField(label="State",max_length=150,widget=forms.TextInput(attrs={"placeholder":"State","class":"input validation"}))
    # delivery_type = forms.ChoiceField(label="Delivery Type",widget=forms.RadioSelect, choices=DELIVERY_TYPE)


PAYMENT_TYPE=(
    ('online_Payu','ONLINE PAYUMONEY'),
    ('on_cash','ON CASH')
)
DELIVERY_TIME = (
    ('10am_12pm','10:00 am - 12:00 pm'),
    ('12pm_02pm','12:00 pm - 02:00 pm'),
    ('02pm_04pm','02:00 pm - 04:00 pm'),
    ('04pm_06pm','04:00 pm - 06:00 pm')
)
class PaymentForm(forms.Form):
    """form for ther Payment"""
    payment_type = forms.ChoiceField(choices = PAYMENT_TYPE, label="Payu", initial='on_cash', widget=forms.RadioSelect(attrs={"class":""}), required=True)
    delivery_time = forms.ChoiceField(choices = DELIVERY_TIME, label="Delivery Time", initial='10am_12pm', widget=forms.Select(attrs={"class":"select"}), required=True)

class AddPlantForm(forms.Form):
    """docstring forAddPlantForm."""
    plant = forms.ModelChoiceField(queryset=Plants.objects.all(), empty_label="select plant",widget=forms.Select(attrs={"class":"select-plant select"}))
    quantity = forms.CharField(label="Quantity",widget=forms.NumberInput(attrs={'placeholder':"Quantity","class":"input validation"}))
    # def __init__(self, arg):
    #     superAddPlantForm, self).__init__()
    #     self.arg = arg

class ChangePasswordForm(forms.Form):
    """form for ther user change password"""
    old_password=forms.CharField(label="Old Password",widget=forms.PasswordInput(attrs={"placeholder":"Old Password","class":"input validation"},render_value=True),)
    new_password=forms.CharField(label="New Password",widget=forms.PasswordInput(attrs={"placeholder":"New Password","class":"input validation"},render_value=True),)
    retype_password=forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs={"placeholder":"Confirm New Password","class":"input validation"},render_value=True),)



# class UserProfileForm(forms.Form):
class UserProfileForm(forms.ModelForm):
    """
    Form for serving the profile form
    """
    class Meta:
        model = UserProfile
        fields = ['mobile', 'date_of_birth', 'name']
        widgets = {
            'mobile': forms.NumberInput(attrs={'class':'input','placeholder':'Mobile','required':True}),
            'date_of_birth': forms.TextInput(attrs={'class':'input','placeholder':'Date Of Birth','required':True}),
            'name': forms.TextInput(attrs={'class':'input','placeholder':'Name','required':True})
        }

    def clean(self, *args, **kwargs):
        """
        Clean function
        """
        pass
def validate_pin_code(self,pin):
        """"""
        if not len(str(pin))==6:
            return True
        return False

class UserAddressForm(forms.ModelForm):
    """
    Form for serving the address details
    """
    class Meta:
        model = UserProfile
        fields = ['address_line1', 'address_line2', 'state','city','nearest_landmark','pincode']
        widgets = {
            'address_line1': forms.TextInput(attrs={'class':'input validate','placeholder':'Address Line 1','required':True}),
            'address_line2': forms.TextInput(attrs={'class':'input','placeholder':'Address Line 2','required':True}),
            'state': forms.TextInput(attrs={'class':'input validate','placeholder':'State','required':True}),
            'city': forms.TextInput(attrs={'class':'input validate','placeholder':'City','required':True}),
            'nearest_landmark': forms.TextInput(attrs={'class':'input','placeholder':'Nearest Landmark','required':True}),
            'pincode': forms.NumberInput(attrs={'class':'input validate','placeholder':'pincode','required':True}),
        }

    def clean(self, *args, **kwargs):
        """
        Clean function
        """
        cleaned_data = super(UserAddressForm, self).clean()
        if validate_pin_code(self,cleaned_data.get('pincode')):
            raise forms.ValidationError('Invalid pin, it must consist of six digits')
        else:
            return cleaned_data

class PlantsFieldForm(forms.ModelForm):
    """
    Form for serving the product details
    """
    class Meta:
        model = Plants
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PlantsFieldForm, self).__init__(*args, **kwargs)


    def clean(self,*args, **kwargs):
        """
        Clean function
        """
        cleaned_data = super(PlantsFieldForm, self).clean()
        return cleaned_data

    class Media:
        js = ('/static/plants-field-admin.js',)


class PlantsStockFieldForm(forms.ModelForm):
    """
    Form for serving the product quantity details
    """
    class Meta:
        model = PlantStock
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(PlantsStockFieldForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(userprofile__userType='vendor')

    def clean(self,*args, **kwargs):
        """
        Clean function
        """
        cleaned_data = super(PlantsStockFieldForm, self).clean()
        return cleaned_data

class DeliveryBoyOrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeliveryBoyOrderForm, self).__init__(*args, **kwargs)
        self.fields['delivery_boy'].queryset = User.objects.filter(userprofile__userType='delivery_boy')


class OnlineNerseryCategoryForm(forms.ModelForm):
    """
    Online Nersery Category Forms
    """
    class Meta:
        model = OnlineNerseryCategory
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(OnlineNerseryCategoryForm, self).__init__(*args, **kwargs)
        try:
            self.fields['plants'].queryset = Plants.objects.filter(Q(category=self.instance.category) | Q(category=self.instance.category.parent_category),active=True).distinct()
        except:
            self.fields['plants'].queryset = Plants.objects.filter(active=True)

    def clean(self,*args, **kwargs):
        """
        Clean function
        """
        cleaned_data = super(OnlineNerseryCategoryForm, self).clean()
        return cleaned_data
