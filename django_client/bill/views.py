from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from datetime import datetime
from home.context_processors import hasGroup
from django.contrib import messages
import requests

#CREATE
@login_required
def generate(request, case_id):
    access = request.session.get('access_token')
    if hasGroup(access, 'DOC'):
        c = {}
        c.update(csrf(request))
        c_url = f"http://0.0.0.0:8001/api/case/{case_id}/"
        c_response = requests.delete(c_url, headers={'Authorization': f"Bearer {access}"})
        c['case'] = c_response.json()
        i_url = f"http://0.0.0.0:8003/api/item/"
        i_response = requests.get(i_url, headers={'Authorization': f"Bearer {access}"})
        c['items'] = i_response.json()['results']
        return render(request, 'bill/generate.html', c)
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('home/')

@login_required
def doGenerate(request):
    access = request.session.get('access_token')
    if hasGroup(access, 'DOC'):
        ammount = item.sell_price * quantity
        b = bill(case=c, item=item, quantity=quantity, bill_date=bill_date, bill_details=bill_details, ammount=ammount)
        b.save()
        b_url = "http://0.0.0.0:8002/api/bill/"
        b_response = requests.post(
            b_url, 
            json={
                "case": int(request.POST.get('case')), 
                "item": int(request.POST.get('item')), 
                "quantity": int(request.POST.get('quantity', 1)), 
                "bill_date": datetime.now().strftime("%Y-%m-%d"),
                "bill_details": request.POST.get('description', ''),
                "ammount": ammount
            }, 
            headers={'Authorization': f"Bearer {access}"})
        messages.add_message(request, messages.INFO, 'Successfully Added Medicine.')
        return HttpResponseRedirect('/case/')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home/')

#RETRIEVE
@login_required
def view(request):
    c = {}
    c.update(csrf(request))
    access = request.session.get('access_token')
    if hasGroup(access, 'PAT'):
        c['bills'] = []
        c['isPatient'] = True
        c_url = f"http://0.0.0.0:8001/api/case/"
        c_response = requests.get(c_url, headers={'Authorization': f"Bearer {access}"})
        c_ids = [item['id'] for item in c_response.json()['results']]
        cids_str = ','.join(map(str, c_ids))

        b_url = f"http://0.0.0.0:8002/api/bill/?case__in={cids_str}"
        b_response = requests.get(b_url, headers={'Authorization': f"Bearer {access}"})
        c['bills'] = b_response.json()['results']
    elif hasGroup(access, 'REC'):
        id = request.POST.get('patient', '')
        if id == '':
            c['selectPatient'] = True
            p_url = f"http://0.0.0.0:8000/api/user/?role=PAT"
            p_response = requests.get(p_url, headers={'Authorization': f"Bearer {access}"})
            c['patients'] = p_response.json()['results']
            return render(request, 'bill/view_bill.html', c)
        else:
            c['bills'] = []
            c_url = f"http://0.0.0.0:8001/api/case/?all_data=true?patient={id}"
            c_response = requests.get(c_url, headers={'Authorization': f"Bearer {access}"})
            c_ids = [item['id'] for item in c_response.json()['results']]
            cids_str = ','.join(map(str, c_ids))

            b_url = f"http://0.0.0.0:8002/api/bill/?case__in={cids_str}"
            b_response = requests.get(b_url, headers={'Authorization': f"Bearer {access}"})
            c['bills'] = b_response.json()['results']
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

    bills = c['bills']
    c['paidBills'] = []
    c['pendingBills'] = []
    for b in bills:
        if b['is_paid']:
            c['paidBills'].append(b)
        else:
            c['pendingBills'].append(b)
    return render(request, 'bill/view_bill.html', c)

@login_required
def viewMedicine(request):
    c = {}
    access = request.session.get('access_token')
    if hasGroup(access, 'PAT'):
        c['bills'] = []
        c['isPatient'] = True
        c_url = f"http://0.0.0.0:8001/api/case/"
        c_response = requests.get(c_url, headers={'Authorization': f"Bearer {access}"})
        c_ids = [item['id'] for item in c_response.json()['results']]
        cids_str = ','.join(map(str, c_ids))

        b_url = f"http://0.0.0.0:8002/api/bill/?case__in={cids_str}"
        b_response = requests.get(b_url, headers={'Authorization': f"Bearer {access}"})
        c['bills'] = b_response.json()['results']
        return render(request, 'bill/medicines.html', c)
    else:
        messages.add_message(request, messages.WARNING, 'Access Denied.')
        return HttpResponseRedirect('/home')

#UPDATE
@login_required
def pay(request):
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        ids = request.POST.getlist('ids','123')
        if type(ids)==type([]):
            for id in ids:
                b_url = f"http://0.0.0.0:8002/api/bill/{int(id)}/"
                b_response = requests.patch(
                    b_url, 
                    json={
                        "is_paid": True, 
                    }, 
                    headers={'Authorization': f"Bearer {access}"})
        else:
            b_url = f"http://0.0.0.0:8002/api/bill/{int(ids)}/"
            b_response = requests.patch(
                b_url, 
                json={
                    "is_paid": True, 
                }, 
                headers={'Authorization': f"Bearer {access}"})
        messages.add_message(request, messages.INFO, 'Bill Paid Successfully.')
        return HttpResponseRedirect('/bill/')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')

#DELETE
@login_required
def delete(request, id):
    user = request.user
    access = request.session.get('access_token')
    if hasGroup(access, 'REC'):
        b_url = f"http://0.0.0.0:8002/api/bill/{id}/"
        b_response = requests.delete(
            b_url, 
            headers={'Authorization': f"Bearer {access}"})
        messages.add_message(request, messages.INFO, 'Successfully Deleted Bill.')
        return HttpResponseRedirect('/bill/')
    messages.add_message(request, messages.WARNING, 'Access Denied.')
    return HttpResponseRedirect('/home')
