from django import forms

# forms.py
from django import forms
from admins.models import (
    Names, GeneralInfo, StallType, Trading,
    FairsAttended, Finances, SocialMedia,ApplicantAccount
)

class TestForm(forms.ModelForm):
    class Meta:
        model = ApplicantAccount
        fields = ['email', 'password', ]
         # exclude appid since it's AutoField (primary key)
     
from django import forms
from admins.models import (
    ApplicantAccount, Names, GeneralInfo, StallType, Trading,
    FairsAttended, Finances, SocialMedia
)

class TestForm(forms.ModelForm):
    class Meta:
        model = ApplicantAccount
        fields = ['email', 'password']
        labels = {
            'email': "Email Address",
            'password': "Password",
        }


class NamesForm(forms.ModelForm):
    class Meta:
        model = Names
        fields = ['buisname', 'stallholdername']
        labels = {
            'buisname': "Business Name",
            'stallholdername': "Stallholder Name",
        }


class GeneralInfoForm(forms.ModelForm):
    class Meta:
        model = GeneralInfo
        fields = ['email', 'adress', 'phonenumber', 'tsandcs', 'referral_source', 'aob']
        labels = {
            'email': "Email Address",
            'adress': "Address",
            'phonenumber': "Phone Number",
            'tsandcs': "Terms and Conditions Accepted",
            'referral_source': "How Did You Hear About Us?",
            'aob': "Any Other Business",
        }


class StallTypeForm(forms.ModelForm):
    class Meta:
        model = StallType
        fields = ['rail', 'numtables']
        labels = {
            'rail': "Do You Require a Rail for clothing ?",
            'numtables': "Number of Tables: 1 or 2 ",
        }


class TradingForm(forms.ModelForm):
    class Meta:
        model = Trading
        fields = ['MRDfair', 'productdesc', 'category', 'wherelsesold']
        labels = {
            'MRDfair': "Most recent Daisy fair if n/a put 01/01/2000 ",
            'productdesc': "Product Description",
            'category': "Product Category",
            'wherelsesold': "Where Else Do You Sell?",
        }
        widgets = {
            'MRDfair': forms.DateInput(attrs={'type': 'date'}),
        }


class FairsAttendedForm(forms.ModelForm):
    class Meta:
        model = FairsAttended
        fields = ['yearstrading', 'prevfairs', 'no_prevfairs']
        labels = {
            'yearstrading': "Years Trading",
            'prevfairs': "Names of all fairs attended since june 2024 ",
            'no_prevfairs': "Number of all fairs attended since june 2024",
        }


class FinancesForm(forms.ModelForm):
    class Meta:
        model = Finances
        fields = ['SimEarnings', 'pricerange', 'MRDfairEarnings']
        labels = {
            'SimEarnings': "Earnings at similar events",
            'pricerange': "Typical Price Range",
            'MRDfairEarnings': "Earnings at most recent Daisy fair if n/a put 0",
        }


class SocialMediaForm(forms.ModelForm):
    class Meta:
        model = SocialMedia
        fields = ['weblink', 'somedialinks', 'followers', 'marketingplan']
        labels = {
            'weblink': "Website Link",
            'somedialinks': "Social Media Links",
            'followers': "Number of Followers",
            'marketingplan': "PIVOTAL ANSWER:  How do you plan to market your attendance"
             } 















'''old form below 
class ApcInfo(forms.Form):
    adress = forms.CharField(label='Address', max_length=255)  # CharField 1
    email = forms.CharField(label='email', max_length=255)  # CharField 24
    telephone_number = forms.CharField(label='Telephone Number', max_length=255)  # CharField 2 
    buisname = forms.CharField(label='Business Name', max_length=255)  # CharField 5
    stallholdername = forms.CharField(label='Stallholder Name', max_length=255)  # CharField 23
    yearstrading = forms.IntegerField(label='Years Trading')  # IntegerField 6
    prevfairs = forms.CharField(
        label='Names of fairs attended by your business since June 2024'
    , max_length=255)  # IntegerField 8
    no_prevfairs = forms.IntegerField(
        label='Total number of fairs attended by your business since June 2024'
    )  # IntegerField 9
    simearnings = forms.IntegerField(
        label='average takings at similair events') ## Similair Earnings per day at previous fairs attended aka  # DecimalField 7
    wherelsesold = forms.CharField(label='Where Else Sold', max_length=255)  # CharField 10
    website_link = forms.URLField(label='Website Link', max_length=255)  # URLField 11
    somedialinks = forms.CharField(label='Social Media Links', max_length=255)  # CharField 12
    followers = forms.IntegerField(label='Followers')  # IntegerField 13
    marketingplan = forms.CharField(label='Marketing Plan', max_length=255)  # CharField 14
    productdesc = forms.CharField(label='Product Description', max_length=255)  # CharField 15
    category = forms.CharField(label='Category', max_length=255)  # CharField 16
    MRDfair = forms.CharField(label='MRD Fair', max_length=255)  # CharField 17
    MRDfairearnings = forms.IntegerField(
        label='MRD Fair Earnings')  # DecimalField 18
    pricerange = forms.CharField(label='Price Range', max_length=255)  # CharField 19
    rail = forms.BooleanField(label='Rail?', required=False)  # BooleanField 20
    no_of_tables = forms.IntegerField(label='No of Tables')  # IntegerField 21 
    referral_source = forms.CharField(label='Referral Source', max_length=255)  # CharField 3
    AOB = forms.CharField(label='AOB (Any Other Business)', max_length=255)  # CharField 4
    tsancs = forms.BooleanField(label='Tsancs', required=False)  # BooleanField 22

'''
class LoginForm(forms.Form):
    test = forms.CharField(label='Test', max_length=255)




