from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from datetime import datetime
from home.context_processors import hasGroup
from django.contrib import messages
from rest_framework_simplejwt.tokens import AccessToken
import requests

#CREATE
@login_required
def generate(request):
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        c = {}
        c.update(csrf(request))
        p_url = f"http://0.0.0.0:8000/api/user/?role=PAT"
        p_response = requests.get(p_url, headers={'Authorization': f"Bearer {access}"})
        c['patients'] = p_response.json()['results']
        return render(request, 'case/generate.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def doGenerate(request):
    access = request.session.get('access_token')
    decoded_token = AccessToken(access)
    if hasGroup(access, 'REC'):
        description = request.POST.get('description', '')
        filed_date = datetime.now().strftime("%Y-%m-%d")

        c_url = "http://0.0.0.0:8001/api/case/"
        c_response = requests.post(
            c_url, 
            json= {
                "patient": int(request.POST.get('patient')), 
                "receptionist": decoded_token['uid'], 
                "description": description, 
                "filed_date": filed_date
            }, 
            headers={'Authorization': f"Bearer {access}"})
        if c_response.status_code == 201:
            c = c_response.json()
        else:
            messages.add_message(request, messages.WARNING, 'Create case fail')
        # c = case(patient=patient, receptionist=request.user, description=description, filed_date=filed_date)
        # c.save()

        i_url = f"http://0.0.0.0:8003/api/item/?item_name=Consulting Charges"
        i_response = requests.get(i_url, headers={'Authorization': f"Bearer {access}"})
        if i_response.status_code == 200 and i_response.json()['count'] > 0:
            item = i_response.json()['results'][0]
        else:
            messages.add_message(request, messages.WARNING, 'Not found item Consulting Charges')
        bill_date = datetime.now().strftime("%Y-%m-%d")
        bill_details = 'Basic Consulting Charges'
        ammount = item['sell_price']
        b_url = "http://0.0.0.0:8002/api/bill/"
        b_response = requests.post(
            b_url, 
            json={
                "case": c['id'], 
                "item": item['id'], 
                "quantity": 1, 
                "bill_date": bill_date,
                "bill_details": bill_details,
                "ammount": ammount
            }, 
            headers={'Authorization': f"Bearer {access}"})
        if b_response.status_code == 201:
            messages.add_message(request, messages.INFO, 'Successfully Generated Case')
            return HttpResponseRedirect('/appointments/book')
        else:
            messages.add_message(request, messages.WARNING, 'Create bill fail')
            return HttpResponseRedirect('/case/generate/')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

#RETRIEVE
@login_required
def view(request):
    c = {}
    user = request.user
    cases = None
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        case_url = "http://0.0.0.0:8001/api/case/"
        case_response = requests.get(case_url, headers={'Authorization': f"Bearer {access}"})
        cases = case_response.json()['results']
    elif hasGroup(access, 'PAT'):
        case_url = f"http://0.0.0.0:8001/api/case/"
        case_response = requests.get(case_url, headers={'Authorization': f"Bearer {access}"})
        cases = case_response.json()['results']
    elif hasGroup(access, 'DOC'):
        c['isDoctor'] = True
        case_url = f"http://0.0.0.0:8001/api/case/"
        case_response = requests.get(case_url, headers={'Authorization': f"Bearer {access}"})
        cases = case_response.json()['results']

    open=[]
    closed=[]
    for ca in cases:
        if ca['closed_date']:
            closed.append(ca)
        else:
            open.append(ca)
    c['openCases'] = open
    c['closedCases'] = closed
    return render(request, 'case/view.html', c)

#UPDATE
@login_required
def close(request, id):
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'DOC'):
        c_url = f"http://0.0.0.0:8001/api/case/{id}/"
        c_response = requests.patch(
            c_url, 
            json= {
                "closed_date": datetime.now().strftime("%Y-%m-%d"),
            }, 
            headers={'Authorization': f"Bearer {access}"})
        if c_response.status_code == 200:
            messages.add_message(request, messages.INFO, 'Successfully Closed Case')
            return HttpResponseRedirect('/case')
        else:
            messages.add_message(request, messages.WARNING, 'Close case fail')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')


#DELETE
@login_required
def delete(request, id):
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        c_url = f"http://0.0.0.0:8001/api/case/{id}/"
        c_response = requests.delete(
            c_url, 
            headers={'Authorization': f"Bearer {access}"})
        messages.add_message(request, messages.INFO, 'Successfully delete Case')
        return HttpResponseRedirect('/case')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')
