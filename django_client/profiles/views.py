from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.template.context_processors import csrf
from home.context_processors import hasGroup
from django.contrib import messages
import requests

# Create your views here.
@login_required
def myProfile(request):
    c={}
    access = request.session.get('access_token')
    if hasGroup(access, 'PAT'):
        c['isPatient'] = True
    return render(request, 'profiles/my_profile.html', c)

@login_required
def register(request):
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        c = {}
        c.update(csrf(request))
        return render(request, 'profiles/register.html')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

@login_required
def doRegister(request):
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        username = request.POST.get('username')
        password = request.POST.get('password1')
        cpassword = request.POST.get('password2')
        if not password == cpassword:
            messages.add_message(request, messages.ERROR, 'Passwords not matching.')
            return HttpResponseRedirect('/profile/register')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        # contact_no = request.POST.get('contact_no')
        # if not contact_no.isdigit():
        #     messages.add_message(request, messages.ERROR, 'Wrong Contact no.')
        #     return HttpResponseRedirect('/profile/register')
        # dob = request.POST.get('dob')
        # blood_group = request.POST.get('blood_group')
        email = request.POST.get('email')
        p_url = "http://0.0.0.0:8000/api/auth/register/"
        p_response = requests.post(
            p_url, 
            json={
                "username": username,
                "password": password,
                "user": {
                    "email": email,
                    "fullname": {
                    "first_name": first_name,
                    "last_name": last_name
                    },
                    "address": {
                        "noHouse": request.POST.get('noHouse'),
                        "street": request.POST.get('street'),
                        "district": request.POST.get('district'),
                        "city": request.POST.get('city'),
                        "country": request.POST.get('country')
                    }
                }
            }, 
            headers={'Authorization': f"Bearer {access}"})

        messages.add_message(request, messages.WARNING, 'Successfully Registered '+username)
        return HttpResponseRedirect('/case/generate')
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')
