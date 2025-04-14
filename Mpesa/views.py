from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from.models import Transaction
from Mpesa.Authorization import get_mpesa_access_token
from django.conf import settings
import requests
from datetime import datetime
import base64
from django.contrib.auth.decorators import login_required
from Store.models import Product
from django.shortcuts import get_object_or_404



@csrf_exempt
def c2b_validation(request):
    print("Validation Triggered")

    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        body_unicode = request.body.decode('utf-8')
        print("Raw Validation Body:", repr(body_unicode))

        if not body_unicode.strip():
            print("Empty body in validation")
            return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted - No content"})

        data = json.loads(body_unicode)
        print(" Parsed Validation Data:", data)

    except json.JSONDecodeError as e:
        print(" JSONDecodeError in validation:", str(e))
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted - Invalid JSON"}, status=200)

    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

@csrf_exempt
def c2b_confirmation(request):
    print('confirmation Triggered')
    data = json.loads(request.body)
    print("C2B Confirmation Data:", data)

    
    #used get to prevent key error in case the key is not found
    transaction_id = data.get("TransactionID")
    short_code = data.get("ShortCode")
    msisdn = data.get("MSISDN")
    amount = data.get("Amount")
    bill_ref_number = data.get("BillRefNumber")
    
   
    transaction = Transaction.objects.create(
        transaction_id=transaction_id,
        short_code=short_code,
        msisdn=msisdn,
        amount=amount,
        bill_ref_number=bill_ref_number,
        status='Completed'  
    )
    #confirmation_info = transaction()
    print("Confirmation Info:", transaction)
    # Return a response confirming the data receipt
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Received"})

  
@csrf_exempt
def simulate_payment(request):
    print(" simulate_payment called")
    access_token = get_mpesa_access_token()
    print(" token:", access_token)

    # Payload
    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,  
        "CommandID": "CustomerPayBillOnline",  
        "Amount": 10,  
        "Msisdn": "254708374149",  
        "BillRefNumber": "INV001"  
    }

 
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"

    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Simulation endpoint request
    response = requests.post(url, json=payload, headers=headers)
    print("📥 status:", response.status_code, "body:", response.json())


    if response.status_code == 200:
        data = response.json()
        print("Simulation Response:", data)
        return JsonResponse(data)  

    else:
        return JsonResponse({"error": "Failed to simulate payment", "status_code": response.status_code})
    



# STK PUSH
@csrf_exempt
@login_required
def lipa_na_mpesa_online(request, product_id):
    if request.method =="POST":
       ## data = json.loads(request.body)
        user = request.user
        phone_number = user.phone_number

        product = get_object_or_404(Product, pk=product_id)
        amount = int(product.price)
        
        access_token = get_mpesa_access_token()

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((settings.BUSINESS_SHORTCODE + settings.MPESA_PASSKEY + timestamp).encode()).decode()

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": settings.BUSINESS_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,  # change as needed
            "PartyA": phone_number,  # test phone number
            "PartyB": settings.BUSINESS_SHORTCODE,
            "PhoneNumber": phone_number,  # same as PartyA
            "CallBackURL": settings.STK_CALLBACK_URL,
            "AccountReference": "Test Payment",
            "TransactionDesc": "Paying for testing"
        }

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            headers=headers,
            json=payload
        )

        return JsonResponse(response.json())
    else:
        return HttpResponse("Only Post allowed for now")


@csrf_exempt
def stk_callback(request):
    print(" STK Callback Triggered")

    raw_body = request.body.decode('utf-8')
    print(f" Raw STK Body: {raw_body!r}")

    if not raw_body:
        print(" Empty body in STK callback")
        return HttpResponseBadRequest("Empty body")

    try:
        data = json.loads(raw_body)
        print(f" Parsed JSON: {json.dumps(data, indent=2)}")
    except json.JSONDecodeError as e:
        print(f" JSON Decode Error: {e}")
        return HttpResponseBadRequest("Invalid JSON")

   
    return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})