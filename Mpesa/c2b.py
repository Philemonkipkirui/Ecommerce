import requests
from django.conf import settings
from Mpesa.Authorization import get_mpesa_access_token

def register_c2b_urls():
    access_token = get_mpesa_access_token()
    register_url = f"{settings.MPESA_BASE_URL}/mpesa/c2b/v1/registerurl"
    
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "ShortCode": settings.MPESA_SHORTCODE,
        "ResponseType": 'Completed',
        "ConfirmationURL": settings.CONFIRMATION_URL,
        "ValidationURL": settings.VALIDATION_URL
    }

    print("Register URL:", register_url)
    print("Register Payload:", payload)


    response = requests.post(register_url, json=payload, headers=headers)
    return response.json()
