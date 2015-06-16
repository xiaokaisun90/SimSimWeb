from django import forms
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
    # property_id = forms.IntegerField()
    requested_access_start_time = forms.CharField()
    requested_access_end_time = forms.CharField()
    # request_access_time_stamp = forms.IntegerField()
    repeat = forms.BooleanField()
    # access_times = forms.BooleanField()

    # class Meta:
    #     model = GuestAccessRequestQueue
    #     exclude = ()

    def clean(self):
        cleaned_data = super(GuestAccessRequestForm, self).clean()



        mobile_phone_number = self.cleaned_data.get('mobile_phone_number')
        print mobile_phone_number
        requested_access_start_time = self.cleaned_data.get('requested_access_start_time')
        repeat = self.cleaned_data.get('repeat')
        requested_access_end_time = self.cleaned_data.get('requested_access_end_time')

        if not mobile_phone_number:
            return forms.ValidationError('You should enter the mobile phone number')
        if not requested_access_start_time:
            return forms.ValidationError('You should enter requested_access_start_time')
        if not requested_access_end_time:
            return forms.ValidationError('You should enter requested_access_end_time')
        return self.cleaned_data

