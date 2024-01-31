import base64
import requests
import json
from datetime import datetime 
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Call

@csrf_exempt
def home(request):
    if request.method == "POST":
        try:
            event = request.POST.get('event')
            from_number = request.POST.get('from')
            to_number = request.POST.get('to')
            direction = request.POST.get('direction')
            call_id = request.POST.get('callId')
            user = request.POST.get('user[]')
            user_id_list = request.POST.get('userId[]')
            user_id_list1 = request.POST.get('userId1[]')
            full_user_id_list = request.POST.get('fullUserId[]')

            call = Call(
                event=event,
                from_number=from_number,
                to_number=to_number,
                direction=direction,
                call_id=call_id,
                user=user,
                user_id_list=user_id_list,
                user_id_list1=user_id_list1,
                full_user_id_list=full_user_id_list
            )
            call.save()
            return HttpResponse("Data saved successfully", status=200)
        except Exception as e:
            print("Error processing JSON data:", str(e))
            return HttpResponse("Bad Request", status=400)

    url = "https://api.sipgate.com/v2"
    result = requests.get(url)

    if result.status_code == 200:
        token_id = 'token-5KIN89'
        token = 'c533fb19-c9f9-412b-a37e-b91aeb9b1519'
        base_url = 'https://api.sipgate.com/v2'
        credentials = (token_id + ':' + token).encode('utf-8')
        base64_encoded_credentials = base64.b64encode(credentials).decode('utf-8')
        headers = {'Authorization': 'Basic ' + base64_encoded_credentials}

        response = requests.get(base_url + '/contacts/internal', headers=headers)
        response_body = response.content.decode("utf-8")
        response_data = json.loads(response_body)
        context = {'items': response_data.get('items', [])}

        return render(request, 'home.html', {'context': context})

    return HttpResponse('Something went wrong')


def outgoing_call(request):
    if request.method == 'POST':
        try:
            callee = request.POST.get('callee')
            print(callee)

            device_id = "your_device_id"
            caller = "your_caller_phone_number"
            caller_id = "your_caller_id"

            token = "token-5KIN89"
            token_id = "c533fb19-c9f9-412b-a37e-b91aeb9b1519"

            base_url = 'https://api.sipgate.com/v2'

            headers = {
                'Content-Type': 'application/json'
            }

            request_body = {
                "deviceId": device_id,
                "callee": callee,
                "caller": caller,
                "callerId": caller_id
            }

            response = requests.post(
                base_url + '/sessions/calls',
                json=request_body,
                auth=requests.auth.HTTPBasicAuth(token_id, token),
                headers=headers
            )

            print('Status:', response.status_code)
            print('Body:', response.content.decode("utf-8"))

            return JsonResponse({'message': 'Outgoing call initiated successfully'})
        except Exception as e:
            print('Error making outgoing call:', str(e))
            return JsonResponse({'error': 'Failed to initiate outgoing call'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)



def fetch_history(request):
    if request.method == 'GET':
        try:
            token_id = 'token-5KIN89'
            token = 'c533fb19-c9f9-412b-a37e-b91aeb9b1519'
            base_url = 'https://api.sipgate.com/v2/history' 
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
    calls_data = Call.objects.all() 

    context = {'calls_data': calls_data}

    return render(request, 'Logs.html', context)