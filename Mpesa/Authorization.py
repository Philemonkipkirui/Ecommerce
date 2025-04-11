import base64
import requests
from django.conf import settings
from django.core.cache import cache


def get_mpesa_access_token():
    """
    Fetches (and caches) an M-Pesa OAuth token.
    """
    # Try cache first
    token = cache.get('mpesa_access_token')
    if token:
        return token

    # Build the URL
    url = settings.MPESA_BASE_URL + settings.MPESA_AUTH_ENDPOINT

    # Basic auth header: base64(CONSUMER_KEY:CONSUMER_SECRET)
    credentials = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode()

    headers = {
        'Authorization': f'Basic {encoded}',
        'Cache-Control': 'no-cache',
    }

    # Send the GET request
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    # Example response:
    # {
    #   "access_token": "ACCESS_TOKEN",
    #   "expires_in": "3600"
    # }
    access_token = data['access_token']
    expires_in = int(data.get('expires_in', 3600))

    # Cache it slightly less than expiry
    cache.set('mpesa_access_token', access_token, timeout=expires_in - 60)
    return access_token
