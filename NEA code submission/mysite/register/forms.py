from django import forms


class Aplogin(forms.Form):
    emailadress = forms.CharField(label='Email Address', max_length=255)
    password = forms.CharField(label='Password', max_length=255)


class Adlogin(forms.Form):
    emailadress = forms.CharField(label='Email Address', max_length=255)
    password = forms.CharField(label='Password', max_length=255)
    member_code = forms.IntegerField(label='Member Code')


class SignupForm(forms.Form):
    emailadress1 = forms.CharField(label='Email Address', max_length=255)
    password = forms.CharField(label='Password', max_length=255)
    password1 = forms.CharField(label='Confirm Password', max_length=255)