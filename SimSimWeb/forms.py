import re
from django import forms
from django.forms import CharField
from django.core.validators import RegexValidator


from SimSimWeb.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    primary_mobile_number = forms.IntegerField()
    password1 = forms.CharField(max_length=30,
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=30,
                                widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        return cleaned_data

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    def clean_primary_mobile_number(self):
        primary_mobile_number = self.cleaned_data.get('primary_mobile_number')
        return primary_mobile_number

class GuestAccessRequestForm(forms.Form):
    mobile_phone_number = forms.IntegerField()
    property_id = forms.IntegerField()
    requested_access_start_time = forms.DateTimeField()
    requested_access_end_time = forms.DateTimeField()
    request_access_time_stamp = forms.IntegerField()
    repeat = forms.BooleanField()
    access_times = forms.BooleanField()

    # class Meta:
    #     model = GuestAccessRequestQueue
    #     exclude = ()

    def clean(self):
        cleaned_data = super(GuestAccessRequestForm, self).clean()
        return cleaned_data
        
        #
        # property_id = self.cleaned_data.get('property_id')
        # mobile_phone_number = self.cleaned_data.get('mobile_phone_number')
        # requested_access_start_time = self.cleaned_data.get('requested_access_start_time')
        # requested_access_end_time = self.cleaned_data.get('requested_access_end_time')
        #
        # if not property_id:
        #     return forms.ValidationError('You should select the property')
        # if not mobile_phone_number:
        #     return forms.ValidationError('You should enter the mobile phone number')
        # if not requested_access_start_time:
        #     return forms.ValidationError('You should enter requested_access_start_time')
        # if not requested_access_end_time:
        #     return forms.ValidationError('You should enter requested_access_end_time')


class selectPropertyForm(forms.Form):
    property = forms.ModelChoiceField(queryset = Properties.objects.all(), widget=forms.Select(attrs={'class': 'form-control input-xlarge select2me', 'onChange': 'select_property.submit()'}), label = '' )



class familyMemberForm(forms.Form):
    username = forms.CharField(label = 'Name', widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': 'Sanny'}))
    mobile = forms.CharField(label = 'Mobile', validators=[RegexValidator(regex='\A(\d{10}|\(?\d{3}\)?[-. ]\d{3}[-.]\d{4})$', message='Please Enter a valid 10-digit number', code=None)], widget = forms.TextInput(attrs = {'class': 'form-control', 'placeholder': '123-456-7890'}))

    def clean(self):
        cleaned_data = super(familyMemberForm, self).clean()
        username = cleaned_data.get('username')
        mobile = cleaned_data.get('mobile')
        number = UserInfo.objects.filter(primary_mobile_number = mobile)
        if (len(self.errors) == 0):
            if not number:
                msg = "The number you entered doesn't exist"
                self.add_error('mobile', msg)
            else:
                validateUsername = UserInfo.objects.get(primary_mobile_number = mobile).user_id.username
                if username != validateUsername:
                    msg = "The username doesn't match the mobile"
                    self.add_error('username', msg)



    def process_mobile(self):
        data = self.cleaned_data['mobile']
        mobile = re.sub(r'[- ()]',r'', data)
        return mobile 