import base64
import requests
import json
from datetime import datetime 
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .models import *

base_url = 'https://api.sipgate.com/v2/history' 
token_id = 'token-5KIN89'
token = 'c533fb19-c9f9-412b-a37e-b91aeb9b1519'
            
@csrf_exempt
def home(request):
    if request.method == "POST":
        try:
            selected_user_id = 1  
            data = json.loads(request.body.decode('utf-8'))
            selected_user_id = data.get('user_id')
            selected_user = str(selected_user_id) 
            print(selected_user)
            if selected_user.isdigit():
                user_data = get_object_or_404(SipgateUser, id=int(selected_user))
                user_data = [user_data]  
            else:
                user_data = []
            
            contact_data = CompanyContact.objects.all()
            device_data = Devices.objects.all()

            context = {
                'contact_data': contact_data,
                'user_data': user_data,
                'device_data': device_data,
            }
            return render(request, 'home.html', {'context': context})
        except Exception as e:
            print("Error processing JSON data:", str(e))
            return HttpResponse("Bad Request", status=400)
    else:
        all_users = SipgateUser.objects.all()

        context = {
            'contact_data': CompanyContact.objects.all(),
            'user_data': all_users,
            'device_data': Devices.objects.all(),
        }
        return render(request, 'home.html', {'context': context})


def outgoing_call(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            callee = data.get('callee')
            username = data.get('username')
            callee = str(callee)
            device_id = "e0"
            caller = "e0"
            caller_id = "0211-87973990565"
            credentials = (token_id + ':' + token).encode('utf-8')
            base64_encoded_credentials = base64.b64encode(credentials).decode('utf-8')

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + base64_encoded_credentials
            }

            request_body = {
                "deviceId": device_id,
                "callee": callee,
                "caller": caller,
                "callerId": caller_id
            }

            response = requests.post(
                base_url + '/sessions/calls',
                headers=headers,
                json=request_body,
            )

            print('Status:', response.status_code)
            print('Body:', response.content.decode("utf-8"))

            device, created = Devices.objects.get_or_create(device_id=device_id, defaults={'caller_id': caller_id})

            # Save CallLog
            logs = CallLog(
                device=device,
                called_on_number=callee,
                date=datetime.now(),
                call_type=True, 
                caller=username,
                caller_id=device.caller_id, 
            )
            logs.save()

            return JsonResponse({'message': 'Outgoing call initiated successfully'})
        except Exception as e:
            print('Error making outgoing call:', str(e))
            return JsonResponse({'error': 'Failed to initiate outgoing call'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)





def fetch_history(request):
    if request.method == 'GET':
        try:
            credentials = (token_id + ':' + token).encode('utf-8')
            base64_encoded_credentials = base64.b64encode(credentials).decode('utf-8')
            headers = {'Authorization': 'Basic ' + base64_encoded_credentials}

            response = requests.get(base_url, headers=headers)
            response_data = response.json()

            call_logs = response_data.get('items', [])

            for log in call_logs:
                created_time = datetime.strptime(log['created'], "%Y-%m-%dT%H:%M:%SZ")
                last_modified_time = datetime.strptime(log['lastModified'], "%Y-%m-%dT%H:%M:%SZ")
                duration_seconds = int((last_modified_time - created_time).total_seconds())
                log['duration'] = divmod(duration_seconds, 60)

            context = {'call_logs': call_logs}
            return render(request, 'callLogs.html', context)
        except Exception as e:
            print('Error fetching history:', str(e))
            return JsonResponse({'error': 'Failed to fetch history'}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


    
def Logs(request):
    phone_numbers = set(CompanyContact.objects.values_list('phone_number', flat=True))
    logs_data = CallLog.objects.all()
    results = []
    for log in logs_data:
        if log.called_on_number in phone_numbers:
            results.append('In contacts')
        else:
            results.append('Unknown')
    context = {'logs_data': zip(logs_data, results)}

    return render(request, 'Logs.html', context)



#  if request.method == "POST":
#         try:
           
#             data = json.loads(request.body.decode('utf-8'))
#             event = data.get('event')
#             from_number = data.get('from')
#             to_number = data.get('to')
#             direction = data.get('direction')
#             call_id = data.get('callId')
#             user = data.get('user[]')
#             user_id_list = data.get('userId[]')
#             user_id_list1 = data.get('userId1[]')
#             full_user_id_list = data.get('fullUserId[]')

#             call = Call(
#                 event=event,
#                 from_number=from_number,
#                 to_number=to_number,
#                 direction=direction,
#                 call_id=call_id,
#                 user=user,
#                 user_id_list=user_id_list,
#                 user_id_list1=user_id_list1,
#                 full_user_id_list=full_user_id_list
#             )
#             call.save()
#             return HttpResponse("Data saved successfully", status=200)

#         except Exception as e:
#             print("Error processing JSON data:", str(e))
#             return HttpResponse("Bad Request", status=400)