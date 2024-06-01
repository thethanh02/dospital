from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from datetime import datetime
from django.utils import timezone
from home.context_processors import hasGroup
from django.contrib import messages
from rest_framework_simplejwt.tokens import AccessToken
import requests


#CREATE
@login_required
def book(request):
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        c = {}
        c.update(csrf(request))
        case_url = f"http://0.0.0.0:8001/api/case/?all_data=true"
        case_response = requests.get(case_url, headers={'Authorization': f"Bearer {access}"})
        p_url = f"http://0.0.0.0:8000/api/user/?role=PAT"
        p_response = requests.get(p_url, headers={'Authorization': f"Bearer {access}"})
        d_url = f"http://0.0.0.0:8000/api/user/?role=DOC"
        d_response = requests.get(d_url, headers={'Authorization': f"Bearer {access}"})
        c['patients'] = p_response.json()['results']
        c['doctors'] = d_response.json()['results']
        c['cases'] = case_response.json()['results']
        return render(request, 'appointments/book_appointment.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def doBook(request):
    user = request.user
    access = request.session.get('access_token')
    decoded_token = AccessToken(access)
    if hasGroup(access, 'REC'):
        appointment_time = request.POST.get('appointment_date')+'T'+request.POST.get('appointment_time')
        # appointment_time = datetime(*[int(v) for v in appointment_time.replace('T', '-').replace(':', '-').split('-')])
        a_url = "http://0.0.0.0:8001/api/appointment/"
        a_response = requests.post(
            a_url, 
            json={
                "patient": int(request.POST.get('patient')), 
                "doctor": int(request.POST.get('doctor')), 
                "receptionist": decoded_token['uid'], 
                "case": int(request.POST.get('case')),
                "appointment_time": appointment_time,
            }, 
            headers={'Authorization': f"Bearer {access}"})
        if a_response.status_code == 201:
            messages.add_message(request, messages.INFO, 'Appointment Successfully Booked')
        else:
            messages.add_message(request, messages.INFO, 'Appointment Book fail')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/appointments/')


#RETRIEVE
@login_required
def view(request):
    c = {}
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        c['isReceptionist'] = True
        c_url = f"http://0.0.0.0:8001/api/appointment/"
        c_response = requests.get(c_url, headers={'Authorization': f"Bearer {access}"})
        c['appointments'] = c_response.json()['results']
    elif hasGroup(access, 'PAT'):
        c_url = f"http://0.0.0.0:8001/api/appointment/"
        c_response = requests.get(c_url, headers={'Authorization': f"Bearer {access}"})
        c['appointments'] = c_response.json()['results']
    elif hasGroup(access, 'DOC'):
        c_url = f"http://0.0.0.0:8001/api/appointment/"
        c_response = requests.get(c_url, headers={'Authorization': f"Bearer {access}"})
        c['appointments'] = c_response.json()['results']
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')
    return render(request, 'appointments/view_all.html', c)


#UPDATE
@login_required
def changeAppointment(request, id):
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        c_url = f"http://0.0.0.0:8001/api/appointment/{id}/"
        c_response = requests.get(c_url, headers={'Authorization': f"Bearer {access}"})
        c = {'appointment': c_response.json()}
        p_url = f"http://0.0.0.0:8000/api/user/?role=DOC"
        p_response = requests.get(p_url, headers={'Authorization': f"Bearer {access}"})
        c['doctors'] = p_response.json()['results']
        c.update(csrf(request))
        return render(request, 'appointments/change.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

@login_required
def doChange(request):
    user = request.user
    access = request.session.get('access_token')
    decoded_token = AccessToken(access)
    if hasGroup(access, 'REC'):
        appointment_time = request.POST.get('appointment_date')+'T'+request.POST.get('appointment_time')
        a_url = "http://0.0.0.0:8001/api/appointment/"
        a_response = requests.patch(
            a_url, 
            json={
                "doctor": int(request.POST.get('doctor')), 
                "receptionist": decoded_token['uid'], 
                "appointment_time": appointment_time,
            }, 
            headers={'Authorization': f"Bearer {access}"})
        if a_response.status_code == 200:
            messages.add_message(request, messages.INFO, 'Appointment Successfully updated')
        else:
            messages.add_message(request, messages.INFO, 'Appointment update fail')
    messages.add_message(request, messages.INFO, 'Appointment Successfully Changed')
    return HttpResponseRedirect('/appointments/')

#DELETE
def delete(request, id):
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        a_url = f"http://0.0.0.0:8001/api/appointment/{id}/"
        a_response = requests.delete(
            a_url, 
            headers={'Authorization': f"Bearer {access}"})
        messages.add_message(request, messages.INFO, 'Appointment Successfully Deleted')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/appointments/')
