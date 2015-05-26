from django import forms
from SimSimWeb.models import *

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=30)
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

    # def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     if User.objects.filter(username__exact=username):
    #         raise forms.ValidationError("Username is already taken.")
    #     return username