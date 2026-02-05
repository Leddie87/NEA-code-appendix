from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import logout 
from django.contrib import messages
import datetime
from datetime import date
from .models import (
    Names, GeneralInfo, StallType, Trading,
    FairsAttended, Finances, SocialMedia,ApplicantAccount,Auth_User, Status
)
from .forms import (
    UpdateForm)
#####        '''merge sort'''

import datetime

def merge_sort(records, key=lambda x: x, reverse=True):
    if len(records) <= 1:
        return records

    mid = len(records) // 2
    left = merge_sort(records[:mid], key=key, reverse=reverse)
    right = merge_sort(records[mid:], key=key, reverse=reverse)

    return merge(left, right, key, reverse)


def merge(left, right, key, reverse):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val = key(left[i])
        right_val = key(right[j])

        # Decide comparison based on `reverse`
        if (left_val > right_val and reverse) or (left_val < right_val and not reverse):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result











# Home page
def home(request):
    if request.method == "POST": 
      Update_form = UpdateForm(request.POST, prefix='updates') 
      if Update_form.is_valid():
            upform_instance = Update_form.save(commit=False)
            upform_instance.user_id = request.user.id
            upform_instance.save()
            messages.success(request, 'Update sent successfully to all applicants!')
            return redirect('/admins/home/')  # Redirect to clear the form

    else:
     Update_form = UpdateForm(prefix='updates')
     messages.error(request, 'This is over 256 characters please submit smaller messages in future')

    total_count = Status.objects.count()
    unreviewed_count = Status.objects.filter(reviewed=False).count()
    accepted_count = Status.objects.filter(accepted=True).count()
    denied_count = Status.objects.filter(denied=True).count()

    context = {
        'Update_form': Update_form,
        'total_count': total_count,
        'unreviewed_count': unreviewed_count,
        'accepted_count': accepted_count,
        'denied_count': denied_count,
    }

    return render(request, 'main/home.html',{'Update_form': Update_form,
        'total_count': total_count,
        'unreviewed_count': unreviewed_count,
        'accepted_count': accepted_count,
        'denied_count': denied_count, })

def gone(request):
    logout(request)
    return render(request, 'main/gone.html', {})

# User accounts (using ORM instead of raw SQL)
def useraccs(request):

   # unreviewed_status_records = Status.objects.filter(
    #    reviewed = False,
    #    user_id= request.user.id
     ## ).select_related('buisname')'''
    #Display_User = []
   # for status_record in unreviewed_status_records:
    #    if status_record.buisname:
     #       Display_User.append({
      #          'user_id': status_record.user_id,
       #         'buisname': status_record.buisname.buisname,
         #       'stallholdername': status_record.buisname.stallholdername,
        #        'comments': status_record.buisname.comments,
          #  })

 #   Display_User = Status.objects.filter(
 #       reviewed=False,
  #  ).select_related('buisname')
    Display_User = []
    for status in Status.objects.filter(reviewed=False).select_related('buisname'):
        if status.buisname:
           Display_User.append({
            'user_id': status.user_id,
            'buisname': status.buisname.buisname,
            'stallholdername': status.buisname.stallholdername,
            'comments': status.buisname.comments,
        })
    

    if request.method == 'POST':
     user_id = request.POST.get('user_id')
     action = request.POST.get('action')

     if user_id and action:
        status_record = get_object_or_404(Status, user_id=user_id)

        if action == 'accept':
            status_record.accepted = True
            status_record.reviewed = True
            status_record.denied = False
        elif action == 'deny':
            status_record.denied = True
            status_record.reviewed = True
            status_record.accepted = False
        elif action == 'comment':
            comment_text = request.POST.get('comment_text')
            if comment_text:
                    # fetch related Names record
                    names_record = get_object_or_404(Names, user_id=user_id)
                    names_record.comments = comment_text
                    names_record.save()
        status_record.save()
        
    template = loader.get_template('main/useraccst.html')
    context = {
        'Display_User': Display_User,
    }

    return HttpResponse(template.render(context, request))


##if request.method == 'POST':
        # Get the user_id from the hidden input
       ## user_id = request.POST.get('user_id')
       ## if user_id:
            # Fetch the status record for this user
          ###  status_record = get_object_or_404(Status, user_id=user_id)
            
            # Update the accepted column
           ## status_record.accepted = True
           ## status_record.reviewed = True
           ## status_record.save()



# Trading page
def trading(request):
    # Fetch and sort trading records
    records = []
    for trade in Trading.objects.select_related('buisname').all():
        if trade.buisname:
            records.append({
                'user_id': trade.user_id,
                'buisname': trade.buisname,
                'MRDfair': trade.MRDfair,
                'productdesc': trade.productdesc,
                'category': trade.category,
                'wherelsesold': trade.wherelsesold,
                'status': getattr(trade, 'status', None),
            })

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id and action:
            status_record = get_object_or_404(Status, user_id=user_id)

            if action == 'accepttrading':
                status_record.accepted = True
                status_record.reviewed = True
                status_record.denied = False
            elif action == 'denytrading':
                status_record.denied = True
                status_record.reviewed = True
                status_record.accepted = False
            status_record.save()

    # Sort records by MRD fair date (most recent first)
    sorted_records = sorted_records =   merge_sort(records, key=lambda x: x.get('MRDfair') or date.min)

    # Fetch all statuses in one query
    statuses = {s.user_id: s for s in Status.objects.all()}

    # Attach status to each record instance
    for record in sorted_records:
        record['status'] = statuses.get(record['user_id'])

    return render(request, 'main/trading.html', {
        'trading_records': sorted_records
    })


# Marketing page
def med_mark(request):
    # Fetch and sort social media records
    records = []
    for social in SocialMedia.objects.select_related('buisname').all():
        if social.buisname:
            records.append({
                'user_id': social.user_id,
                'buisname': social.buisname,
                'weblink': social.weblink,
                'somedialinks': social.somedialinks,
                'followers': social.followers,
                'marketingplan': social.marketingplan,
                'status': getattr(social, 'status', None),
            })

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id and action:
            status_record = get_object_or_404(Status, user_id=user_id)

            if action == 'acceptm':
                status_record.accepted = True
                status_record.reviewed = True
                status_record.denied = False
            elif action == 'denym':
                status_record.denied = True
                status_record.reviewed = True
                status_record.accepted = False
            status_record.save()

    # Sort records by followers (highest first)
    sorted_records = sorted_records = merge_sort(records, key=lambda x: x.get('followers') or 0)

    # Fetch all statuses in one query
    statuses = {s.user_id: s for s in Status.objects.all()}

    # Attach status to each record instance
    for record in sorted_records:
        record['status'] = statuses.get(record['user_id'])

    return render(request, 'main/med_mark.html', {
        'socialmedia_records': sorted_records
    })


# Finances page

def finances(request):
    # Fetch and sort finance records
    records = []
    for finance in Finances.objects.select_related('buisname').all():
     if finance.buisname:
      records.append({
            'user_id': finance.user_id,
            'buisname': finance.buisname,
            'yearstrading': finance.yearstrading,
            'SimEarnings': finance.SimEarnings,
            'pricerange': finance.pricerange,
            'MRDfair': finance.MRDfair,             # date
            'MRDfairEarnings': finance.MRDfairEarnings,
            'status': getattr(finance, 'status', None),  # for accept/deny highlighting
        }) 
    sorted_records =   merge_sort(records, key=lambda x: x.get('MRDfairEarnings') or 0)

    if request.method == 'POST':
     action = request.POST.get('action')
    
    # Sorting actions
     if action == 'sortSEarn':
        sorted_records = merge_sort(records, key=lambda x: x.get('SimEarnings') or 0)
     elif action == 'sortFEarn':
        sorted_records = merge_sort(records, key=lambda x: x.get('MRDfairEarnings') or 0)
     elif action == 'sortYeT':
        sorted_records = merge_sort(records, key=lambda x: x.get('yearstrading') or 0)
     elif action == 'MRDFsort':
        sorted_records =   merge_sort(records, key=lambda x: x.get('MRDfair') or date.min)
        # User-specific actions
     user_id = request.POST.get('user_id')
     action = request.POST.get('action')
     if user_id:
            status_record = get_object_or_404(Status, user_id=user_id)
            if action == 'acceptf':
                status_record.accepted = True
                status_record.reviewed = True
                status_record.denied = False
            elif action == 'denyf':
                status_record.denied = True
                status_record.reviewed = True
                status_record.accepted = False
            status_record.save()

    # Fetch all statuses in one query
    statuses = {s.user_id: s for s in Status.objects.all()}
    # Attach status to each record instance (adds attribute at runtime)
    for record in sorted_records:
      record['status'] = statuses.get(record['user_id'])
    # Now sorted_records already has .status attached
    return render(request, "main/finances.html", {
        "finance_records": sorted_records
    })


#finance_records = Finances.objects.all().values()
# Render template with context
# return render(request, 'main....financs.html', {
# 'finance_records': finance_records  
# Filter Names records where the corresponding Status record has accepted=True
# and link to the current user



# Denied page
def denied(request):
    # Filter Names records where the corresponding Status record has denied=True
    denied_status_records = Status.objects.filter(
        denied=True,
    ).select_related('buisname')

    # Handle actions on denied records
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id and action:
            status_record = get_object_or_404(Status, user_id=user_id)

            if action == 'undo':
                status_record.denied = False
                status_record.reviewed = False
            elif action == 'send_email':
                status_record.emailed = True
            elif action == 'comment':
                comment_text = request.POST.get('comment_text')
                if comment_text:
                    names_record = get_object_or_404(Names, user_id=user_id)
                    names_record.comments = comment_text
                    names_record.save()

            status_record.save()

        # Refresh queryset after possible updates
        _status_records = Status.objects.filter(
            denied=True,
        ).select_related('buisname')
    
    # Get the Names records for the denied status records
    Display_User = []
    for status_record in denied_status_records:
        if status_record.buisname:
            Display_User.append({
                'user_id': status_record.user_id,
                'buisname': status_record.buisname.buisname,
                'stallholdername': status_record.buisname.stallholdername
            })
    
    template = loader.get_template('main/denied.html')
    context = {
        'Display_User': Display_User,
    }
    return HttpResponse(template.render(context, request))


''''
def useraccs(request):
    Display_User = Names.objects.all().values()
    template = loader.get_template('main/useraccst.html')
    context = {
        'Display_User': Display_User,
    }
    if request.method == 'POST':
     user_id = request.POST.get('user_id')
     action = request.POST.get('action')

     if user_id and action:
        status_record = get_object_or_404(Status, user_id=user_id)

        if action == 'accept':
            status_record.accepted = True
            status_record.reviewed = True
        elif action == 'deny':
            status_record.denied = True
            status_record.reviewed = True
        elif action == 'comment':
            comment_text = request.POST.get('comment_text')
            if comment_text:
                    # fetch related Names record
                    names_record = get_object_or_404(Names, user_id=user_id)
                    names_record.comments = comment_text
                    names_record.save()


        status_record.save()

    return HttpResponse(template.render(context, request))
'''
# Application info page
def apcinfo(request):
    # Fetch and sort general info records
    records = []
    for general in GeneralInfo.objects.all():
        records.append({
            'user_id': general.user_id,
            'email': general.email,
            'adress': general.adress,
            'phonenumber': general.phonenumber,
            'tsandcs': general.tsandcs,
            'referral_source': general.referral_source,
            'aob': general.aob,
            'status': getattr(general, 'status', None),
        })

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id and action:
            status_record = get_object_or_404(Status, user_id=user_id)

            if action == 'acceptinfo':
                status_record.accepted = True
                status_record.reviewed = True
                status_record.denied = False
            elif action == 'denyinfo':
                status_record.denied = True
                status_record.reviewed = True
                status_record.accepted = False
            status_record.save()


    sorted_records =   merge_sort(records, key=lambda x: x.get('Muser_id') or 0)

    # Fetch all statuses in one query
    statuses = {s.user_id: s for s in Status.objects.all()}

    # Attach status to each record instance
    for record in sorted_records:
        record['status'] = statuses.get(record['user_id'])

    return render(request, 'main/apcinfo.html', {
        'generalinfo_records': sorted_records
    })

def fairs(request):
    # Fetch and sort fairs attended records
    records = []
    for fair in FairsAttended.objects.select_related('buisname').all():
        if fair.buisname:
            records.append({
                'user_id': fair.user_id,
                'buisname': fair.buisname,
                'yearstrading': fair.yearstrading,
                'prevfairs': fair.prevfairs,
                'no_prevfairs': fair.no_prevfairs,
                'status': getattr(fair, 'status', None),
            })

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id and action:
            status_record = get_object_or_404(Status, user_id=user_id)

            if action == 'acceptfairs':
                status_record.accepted = True
                status_record.reviewed = True
                status_record.denied = False
            elif action == 'denyfairs':
                status_record.denied = True
                status_record.reviewed = True
                status_record.accepted = False
            status_record.save()

    # Sort records by years trading (highest first)
    sorted_records = sorted_records =  merge_sort(records, key=lambda x: x.get('yearstrading') or date.min)

    # Fetch all statuses in one query
    statuses = {s.user_id: s for s in Status.objects.all()}

    # Attach status to each record instance
    for record in sorted_records:
        record['status'] = statuses.get(record['user_id'])

    return render(request, 'main/fairs.html', {
        'fairs_records': sorted_records
    })


def accepted(request):
    accepted_status_records = Status.objects.filter(
        accepted=True,
    ).select_related('buisname')

    # Handle actions on accepted records
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')

        if user_id and action:
            status_record = get_object_or_404(Status, user_id=user_id)

            if action == 'undo':
                status_record.accepted = False
                status_record.reviewed = False
            elif action == 'send_email':
                status_record.emailed = True

            elif action == 'comment':
                comment_text = request.POST.get('comment_text')
                if comment_text:
                    names_record = get_object_or_404(Names, user_id=user_id)
                    names_record.comments = comment_text
                    names_record.save()
            status_record.save()
        # Refresh queryset after possible updates
        accepted_status_records = Status.objects.filter(
            accepted=True,
        ).select_related('buisname')
    # Get the Names records for the accepted status records
    Display_User = []
    for status_record in accepted_status_records:
        if status_record.buisname:
            general_info = GeneralInfo.objects.filter(user_id=status_record.user_id).first()
            names_record = status_record.buisname
            Display_User.append({
                'user_id': status_record.user_id,
                'buisname': names_record.buisname,
                'stallholdername': names_record.stallholdername,
                'comments': names_record.comments,
                'email': general_info.email if general_info else None,
            })
    
    template = loader.get_template('main/accepted.html')
    context = {
        'Display_User': Display_User,
    }
    return HttpResponse(template.render(context, request))








# Email page
def email(request):
    
    user_id = request.POST.get('user_id') or request.GET.get('user_id')
    recipient_email = request.POST.get('recipient_email') or request.GET.get('recipient_email')
    # Accept both 'stallholdername' (from template) and 'stallholder_name'
    stallholder_name = (
     request.POST.get('stallholder_name')
    )
    status_record = None
    error_message = None
    # If user_id is missing but we have an email, resolve user_id from GeneralInfo
    if not user_id and recipient_email:
        resolved_info = GeneralInfo.objects.filter(email=recipient_email).first()
        if resolved_info:
            user_id = resolved_info.user_id

    if user_id:
            # Fetch status for decision
            status_record = Status.objects.select_related('buisname') \
                              .filter(user_id=user_id).first()

            # Fetch recipient email from GeneralInfo unless provided explicitly
            if not recipient_email:
                general_info = GeneralInfo.objects.filter(user_id=user_id).first()
                if general_info:
                    recipient_email = general_info.email
            # Prefer stallholder name from Names via Status.buisname
            if status_record and status_record.buisname and not stallholder_name:
                stallholder_name = status_record.buisname.stallholdername
            if not stallholder_name:
                # Fallback: first Names for the user
                names_record = Names.objects.filter(user_id=user_id).first()
                if names_record:
                    stallholder_name = names_record.stallholdername
    else:
        error_message = "No user selected. Provide user_id via GET/POST or a known recipient_email."

    if not status_record:
        error_message = (error_message or "") + (" " if error_message else "") + "No status found for this user."
    if not recipient_email:
        error_message = (error_message or "") + (" " if error_message else "") + "No email found for this user."

    context = {
        'recipient_email': recipient_email,
        'stallholder_name': stallholder_name,
        'status_record': status_record,
        'error_message': error_message,
    }
    return render(request, 'main/email.html', context)