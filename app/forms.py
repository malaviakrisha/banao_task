from django import forms
from django.contrib.auth.models import User
from .models import Profile
class SignupForm(forms.Form):
    fname = forms.CharField(label="First Name", max_length=150)
    lname = forms.CharField(label="Last Name", max_length=150)
    uname = forms.EmailField(label="Email")
    username1 = forms.CharField(label="Username", max_length=150)
    upass = forms.CharField(label="Password", widget=forms.PasswordInput)
    ucpass = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
    address_line1 = forms.CharField(label="Address Line 1", max_length=255)
    city = forms.CharField(label="City", max_length=100)
    pincode = forms.CharField(label="Pincode", max_length=10)
    photo = forms.ImageField(required=True)  

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("upass")
        confirm_password = cleaned_data.get("ucpass")
        if password != confirm_password:
            raise forms.ValidationError("Password and Confirm Password do not match.")
