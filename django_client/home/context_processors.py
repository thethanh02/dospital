from django.contrib.auth.models import Group
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib import auth
from django.urls import reverse
from datetime import datetime

def hasGroup(access, groupName):
    try:
        decoded_token = AccessToken(access)
        expiration_time = datetime.fromtimestamp(decoded_token['exp'])
        current_time = datetime.now()
        if current_time > expiration_time:
            logout_url = reverse('logout')
            return redirect(logout_url)
        user_role = decoded_token.get('role', None)
        return True if groupName == user_role else False
    except Exception as e:
        return False

def menu_processor(request):
    menu = {}
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'DOC'):
        menu['Appointments'] = '/appointments'
        menu['Cases'] = '/case'
    elif hasGroup(access, 'PAT'):
        # menu['Reports'] = '/reports'
        menu['Appointments'] = '/appointments'
        menu['Medication'] = '/bill/medicines'
        menu['Bills'] = '/bill'
        menu['Cases'] = '/case'
    elif hasGroup(access, 'REC'):
        menu['New Patient'] = '/profile/register'
        menu['Manage Appointments'] = '/appointments'
        menu['New Appointment'] = '/appointments/book'
        menu['Bills'] = '/bill'
        menu['Cases'] = '/case'
        menu['Generate Case'] = '/case/generate'
    elif hasGroup(access, 'LAB'):
        # menu['Reports'] = '/reports'
        menu['Generate Report'] = '/reports/generate'
    elif hasGroup(access, 'INV'):
        menu['All Stock'] = ''
        menu['Stock Details'] = ''

    return {'menu': menu}
