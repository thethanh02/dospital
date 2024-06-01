from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.contrib import messages
from django.contrib.auth.models import User, Group
import requests

def login(request):
	if request.user.is_authenticated:
		messages.add_message(request, messages.INFO, 'You are already Logged in.')
		return HttpResponseRedirect('/home')
	else:
		c = {}
		c.update(csrf(request))
		return render(request, 'loginmodule/login.html', c)

def auth_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	auth_url = 'http://0.0.0.0:8000/api/auth/login/'
	auth_response = requests.post(auth_url, data={'username': username, 'password': password})
	
	if auth_response.status_code == 200:
		tokens = auth_response.json()

		request.session['access_token'] = tokens.get('access')

		user_info_url = 'http://0.0.0.0:8000/api/user/me/'
		user_info_response = requests.get(user_info_url, headers={'Authorization': f"Bearer {tokens.get('access')}"})

		if user_info_response.status_code == 200:
			user_data = user_info_response.json()

			user, created = User.objects.get_or_create(username=username)
			if created:
				user.email = user_data['user']['email']
				# user_data['user']['role']
				user.first_name = user_data['user']['fullname']['first_name']
				user.last_name = user_data['user']['fullname']['last_name']
				user.save()
				
			user_role = user_data['role']
			if user_role == 'DOC':
				user_group = 'doctor'
			elif user_role == 'REC':
				user_group = 'receptionist'
			elif user_role == 'LAB':
				user_group = 'lab_attendant'
			elif user_role == 'INV':
				user_group = 'inventory_manager'
			else:
				user_group = 'patient'

			group, group_created = Group.objects.get_or_create(name=user_group)
			user.groups.add(group)

			user.backend = 'django.contrib.auth.backends.ModelBackend'
			auth.login(request, user)
			messages.add_message(request, messages.INFO, 'Your are now Logged in.')
			return HttpResponseRedirect('/home')
		else:
			messages.add_message(request, messages.WARNING, 'Failed to retrieve user info.')
			return HttpResponseRedirect('/login')
	else:
		messages.add_message(request, messages.WARNING, 'Invalid Login Credentials.')
		return HttpResponseRedirect('/login')

def logout(request):
	if request.user.is_authenticated:
		auth.logout(request)

	if 'access_token' in request.session:
		del request.session['access_token']

	messages.add_message(request, messages.INFO, 'You are Successfully Logged Out')
	messages.add_message(request, messages.INFO, 'Thanks for visiting.')
	return HttpResponseRedirect('/login')
