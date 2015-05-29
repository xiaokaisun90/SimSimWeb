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
    class Meta:
        model = GuestAccessRequestQueue

    def clean(self):
        property_id = self.cleaned_data.get('property_id')
        mobile_phone_number = self.cleaned_data.get('mobile_phone_number')
        requested_access_start_time = self.cleaned_data.get('requested_access_start_time')
        requested_access_end_time = self.cleaned_data.get('requested_access_end_time')
        if not property_id:
            return forms.ValidationError('You should select the property')
        if not mobile_phone_number:
            return forms.ValidationError('You should enter the mobile phone number')
        if not requested_access_start_time:
            return forms.ValidationError('You should enter requested_access_start_time')
        if not requested_access_end_time:
            return forms.ValidationError('You should enter requested_access_end_time')