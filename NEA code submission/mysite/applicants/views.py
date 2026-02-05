from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib.auth import logout
from django.db import transaction
from django.template import loader
from django.contrib import messages
from datetime import date
from .forms import (
    NamesForm,
    GeneralInfoForm,
    StallTypeForm,
    TradingForm,
    FairsAttendedForm,
    FinancesForm,
    SocialMediaForm,
    TestForm,
    NamesForm
)
from admins.models import (
    Names, GeneralInfo, StallType, Trading,
    FairsAttended, Finances, SocialMedia,ApplicantAccount, Status, Updatestable
)



def testform(request):
    if request.method == "POST":
        form = TestForm(request.POST)
        if form.is_valid():
            applicant = form.save(commit=False) # create the instance don't save yet
            applicant.user_id = request.user.id      # assign user's id to the userid column
            applicant.save()                      # now save to DB
            return redirect('apchome')
    else:
        form = TestForm()
    
    return render(request, 'main/testform.html', {'TestForm': form})

def nametest(request):
     if request.method == "POST": 
      names_form = NamesForm(request.POST, prefix='names') 
      # general_info_form = GeneralInfoForm(request.POST, prefix='general')

      forms = [ names_form,] ##''' general_info_form, '''
      if all(f.is_valid() for f in forms):
            names_instance = names_form.save(commit=False)
            names_instance.user_id = request.user.id
            names_instance.save()

            ##general_instance = general_info_form.save(commit= false)
           ## general_instance.user_id = request.user.id
           ## general_instance.save()

     else:
        # GET request: instantiate empty forms with prefixes
            names_form = NamesForm(prefix='names')
           ## general_info_form = GeneralInfoForm(prefix = 'general')

     return render(request, 'main/nametest.html', { 'names_form': names_form,} ,  )



def appform(request):
     if request.method == "POST": 
      names_form = NamesForm(request.POST, prefix='names') 
      general_info_form = GeneralInfoForm(request.POST, prefix='general')
      stall_type_form = StallTypeForm(request.POST, prefix='stall')
      trading_form = TradingForm(request.POST, prefix='trading')
      fairs_attended_form = FairsAttendedForm(request.POST, prefix='fairs')
      finances_form = FinancesForm(request.POST, prefix='finances')
      social_media_form = SocialMediaForm(request.POST, prefix='social')

      forms = [ names_form,general_info_form, stall_type_form, trading_form,fairs_attended_form,finances_form ] ##''' '''
      if all(f.is_valid() for f in forms):
            names_instance = names_form.save(commit=False)
            names_instance.user_id = request.user.id
            names_instance.save()

            general_instance = general_info_form.save(commit=False)
            general_instance.user_id = request.user.id
            general_instance.save()

            stall_instance = stall_type_form.save(commit=False)
            stall_instance.user_id = request.user.id
            stall_instance.save()

            trading_instance = trading_form.save(commit=False)
            trading_instance.user_id = request.user.id
            # only set buisname if names_form validated
            if names_form.is_valid():
             trading_instance.buisname_id = names_instance.pk
             ##   trading_instance.buisname = names_form.cleaned_data.get(Names.buisname)
            trading_instance.save()

            fairs_instance = fairs_attended_form.save(commit=False)
            fairs_instance.user_id = request.user.id
            if names_form.is_valid():
             fairs_instance.buisname_id = names_instance.pk
           ## fairs_instance.SimEarnings_id = None
            fairs_instance.save()

            finances_instance = finances_form.save(commit = False)
            finances_instance.user_id = request.user.id
            if names_form.is_valid():
             finances_instance.buisname_id = names_instance.pk
            if trading_form.is_valid():
                finances_instance.MRDfair = trading_instance.MRDfair
            if fairs_attended_form.is_valid():
                finances_instance.yearstrading = fairs_instance.yearstrading
            finances_instance.save()

            social_instance = social_media_form.save(commit=False)
            social_instance.user_id = request.user.id
            if names_form.is_valid():
             social_instance.buisname_id = names_instance.pk
            social_instance.save()

            status_instance = Status.objects.create(
                user_id=request.user.id,
                buisname_id=names_instance.pk,  # Link to the business name
                reviewed=False,
                starred=False,
                accepted=False,
                denied=False,
                emailed=False,
                fsub = True
            )
            return redirect('apchome')

     else:
        # GET request: instantiate empty forms with prefixes
            names_form = NamesForm(prefix='names')
            general_info_form = GeneralInfoForm(prefix = 'general')
            stall_type_form = StallTypeForm(prefix='stall')
            trading_form = TradingForm(prefix='trading')
            fairs_attended_form = FairsAttendedForm(prefix='fairs')
            finances_form = FinancesForm(prefix='finances')
            social_media_form = SocialMediaForm(prefix='social')

     return render(request, 'main/apform.html', { 'names_form': names_form ,
      'general_info_form' : general_info_form , 'stall_type_form': stall_type_form,  'trading_form': trading_form, 'fairs_attended_form': fairs_attended_form, 'finances_form': finances_form,'social_media_form': social_media_form,
       }   )



 
def gone(request):
   logout(request)
   return render(request, 'main/gone.html', {})
 
#def gone(response):
 #   return render(response, 'main/gone.html', {})

def fsub(response):
    return render(response, 'main/fsub.html', {})
# Create your views here.

def apchome(request):
    status = None
    status_sub = None
    if request.user.is_authenticated:
        try:
            # Get the Status row that corresponds to the logged-in user
            status = Status.objects.get(user_id=request.user.id)
            status_sub = Status.objects.filter(user_id=request.user.id).values('fsub').first()
        except Status.DoesNotExist:
           status = None

    Display_Updates = Updatestable.objects.all().order_by('-recordnum')
    template = loader.get_template('main/apchome.html')
    context = {
        'Display_Updates': Display_Updates, 
        'status': status,
        'status_sub': status_sub,
        }
    return render(request, "main/apchome.html", context)

# Names/Business Names View
