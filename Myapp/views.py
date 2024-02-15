from django.http import HttpResponse, JsonResponse
import base64
import requests
import json
from datetime import datetime 
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from .models import *
import xml.etree.ElementTree as ET
from django.db.models import Q
import re

# ON_HANGUP_URL = "https://de99-138-199-19-168.ngrok-free.app" + "/on-hangup/"
ON_HANGUP_URL = "http://127.0.0.1:8500" + "/on-hangup/"

            
@csrf_exempt
def home(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            selected_user_default_id = data.get('default_id')
            user_data = SipgateUser.objects.filter(id=selected_user_default_id)
            contact_data = CompanyContact.objects.all()
            context = {
                'contact_data': contact_data,
                'user_data': user_data,
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
        }
        return render(request, 'home.html', {'context': context})
    
    
@csrf_exempt
def outgoing_call(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            callee = data.get('callee')
            # username = data.get('username')
            # caller_req = data.get('caller')
            token = request.COOKIES.get('sipgate-token')
            token_id = request.COOKIES.get('sipgate-token_id')
            caller_id = request.COOKIES.get('caller_id')
            caller = request.COOKIES.get('caller')
            default_id = request.COOKIES.get('default_id')
            # active_user_number = request.COOKIES.get('active_user_number')
            credentials = f"{token_id}:{token}"
            base64_encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            base64_encoded_credentials= str(base64_encoded_credentials)
            callee = str(callee)
            try:
                Device_instance = Devices.objects.get(id=default_id)
            except Devices.DoesNotExist:
                return HttpResponse("Device not found", status=404)
            device_id = Device_instance.device_id
            caller = caller
            base_url = 'https://api.sipgate.com/v2/' 

            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic ' + base64_encoded_credentials
            }
            print(headers)
            request_body = {
                "deviceId": device_id,
                "callee": callee,
                "caller": caller,
                "callerId": caller_id,
            }
            print(request_body)

            response = requests.post(
                base_url + 'sessions/calls',
                headers=headers,
                json=request_body, 
            )
            print(response)

            print('Status:', response.status_code)
            print('Body:', response.content.decode("utf-8"))

            # device, created = Devices.objects.get_or_create(device_id=device_id, defaults={'caller_id': caller_id})
            # call = Call.objects.create(
            #     active_user=None,  
            #     company_contact=None,  
            #     event=None,  
            #     from_number=active_user_number,
            #     to_number=callee,
            #     direction="out",
            #     call_id="", 
            #     user=username,
            #     user_id_list=caller_req,
            #     user_id_list1="",
            #     full_user_id_list="",
            #     date=timezone.now(),
            #     modified_time=timezone.now(),
            # )
            # call.save()
            return JsonResponse({'Success': 'Called Successfully'}, status=200)
        except Exception as e:
            print('Error making outgoing call:', str(e))
            return JsonResponse({'error': 'Failed to initiate outgoing call'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)





def fetch_history(request):
    if request.method == 'GET':
        try:
            token = request.COOKIES.get('sipgate-token')
            token_id = request.COOKIES.get('sipgate-token_id')
            credentials = f"{token_id}:{token}"
            base64_encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            base64_encoded_credentials= str(base64_encoded_credentials)
            base_url = 'https://api.sipgate.com/v2/history'
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

def format_phone_number(number):
    number = re.sub(r'\D', '', number)
    
    if number.startswith('+49'):
        number = number[3:]
    elif number.startswith('49'):
        number = number[2:]
    
    if number.startswith('0211'):
        number = number[:4] + '-' + number[4:]
        
    if not number.startswith('0'):
        number = '0' + number
    
    return number

def Logs(request):
    call_logs = Call.objects.all()

    for log in call_logs:
        log.from_number = format_phone_number(log.from_number)
        log.to_number = format_phone_number(log.to_number)
        duration = log.modified_time - log.date
        minutes, seconds = divmod(duration.total_seconds(), 60)
        log.duration = f"{int(minutes)} min {int(seconds)} sec"

    context = {'call_logs': call_logs}
    return render(request, 'Logs.html', context)


incoming_call_flag = False

@csrf_exempt
def incoming_call(request):
    global incoming_call_flag  

    if request.method == "POST":
        try:
            event = request.POST.get('event')
            from_number = request.POST.get('from')
            to_number = request.POST.get('to')
            direction = request.POST.get('direction')
            call_id = request.POST.get('callId')
            user = request.POST.get('user[]')
            user_id_list = request.POST.getlist('userId[]')
            print(user_id_list[0], "194 line")
            user_id_list1 = request.POST.getlist('userId1[]')
            full_user_id_list = request.POST.getlist('fullUserId[]')
            print("webhook", from_number)
            
            if direction == "in":
                matching_contacts = CompanyContact.objects.filter(phone_number__icontains=from_number)
                if matching_contacts.exists():
                    company_contact = matching_contacts.first()
                    print(company_contact.id)
                else:
                    print("Incoming - No matching company contact found.")
                    company_contact = None  
            else:
                matching_contacts = CompanyContact.objects.filter(phone_number__icontains=to_number)
                if matching_contacts.exists():
                    company_contact = matching_contacts.first()
                    print(company_contact.id)
                else:
                    print("outgoing - No company contact found.")
                    company_contact = None  
                    
            if direction == "in":
                modified_to_number = to_number.lstrip('0211')
                sipuser_matching = SipgateUser.objects.filter(
                    Q(caller__icontains=modified_to_number) | 
                    Q(phone_number__icontains=modified_to_number) | 
                    Q(caller_id__icontains=modified_to_number)
                )
            else:
                modified_from_number = from_number.lstrip('0211')
                sipuser_matching = SipgateUser.objects.filter(
                    Q(caller__icontains=modified_from_number) | 
                    Q(phone_number__icontains=modified_from_number) | 
                    Q(caller_id__icontains=modified_from_number)
                )

            if sipuser_matching.exists():
                sipuser = sipuser_matching.first()
                print(sipuser.id)
            else:
                print("No matching company contact found.")
                sipuser = None
            
            print(direction)
            try:
                    
                call = Call(
                    active_user=sipuser,
                    company_contact=company_contact,
                    event=event,
                    from_number=from_number,
                    to_number=to_number,
                    direction=direction,
                    call_id=call_id,
                    user=user,
                    user_id_list=user_id_list,
                    user_id_list1=user_id_list1,
                    full_user_id_list=full_user_id_list,
                    date=datetime.now(),
                    modified_time=datetime.now(),
                )
                call.save()

                # Set the incoming_call_flag to True after saving data
                incoming_call_flag = True

                xml_response = build_xml_response()
                return HttpResponse(xml_response, content_type="application/xml")
            except SipgateUser.DoesNotExist:
                return JsonResponse({"message": "SipgateUser not found"}, status=400)

        except Exception as e:
            print("Error processing form data:", str(e))
            return JsonResponse({"message": "Bad Request"}, status=400)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


def check_incoming_call(request):
    global incoming_call_flag
    phone_numbers = set(CompanyContact.objects.values_list('phone_number', flat=True))
    has_incoming_call = incoming_call_flag
    incoming_call_flag = False

    response_data = {"incomingCall": has_incoming_call}
    if has_incoming_call:
        latest_incoming_call = Call.objects.filter(direction='in').latest('date')
        formatted_from_number = format_phone_number(latest_incoming_call.from_number)
        response_data["contactNumber"] = formatted_from_number
        
        if formatted_from_number in phone_numbers:
            response_data["message"] = "In contacts"
            contact_name = CompanyContact.objects.filter(phone_number=formatted_from_number).values_list('name', flat=True).first()
            response_data["ContactName"] = contact_name if contact_name else "Unknown"
        else:
            response_data["message"] = "Unknown"

    return JsonResponse(response_data)

@csrf_exempt
def on_hangup(request):
    print("The call has been hung up")
    
    if request.method == "POST":
        try:
            call_id = request.POST.get('callId')
            print(call_id)
            try:
                call = Call.objects.get(call_id=call_id)
                print("call")
            except Call.DoesNotExist:
                return JsonResponse({"message": "Call does not exist"}, status=404)

            call.modified_time = datetime.now()
            call.save()
            
            return HttpResponse("This response will be discarded", status=200)
        
        except Exception as e:
            print("Error processing form data:", str(e))
            return JsonResponse({"message": "Bad Request"}, status=400)
    
    return JsonResponse({"message": "Method not allowed"}, status=405)

def build_xml_response():
    response = ET.Element("Response")
    response.set("onHangup", ON_HANGUP_URL)
    xml_response = ET.tostring(response)
    return xml_response

@csrf_exempt
def save_contact(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        csrftoken = data.get('csrftoken')
        print("csrf token", csrftoken)
        print('Received Name:', name)
        print('Received Phone:', phone)

        try:
            CompanyContact.objects.create(name=name, phone_number=phone)
            print('Contact saved successfully')
            return JsonResponse({'message': 'Contact saved successfully'})
        except Exception as e:
            print('Error saving contact:', e)
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)