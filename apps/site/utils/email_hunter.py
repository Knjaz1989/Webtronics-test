import requests

from settings import config


def verify_email(email: str) -> str | None:
    url = 'https://api.hunter.io/v2/email-verifier'
    params = {'email': email, 'api_key': config.HUNTER_API_KEY}
    resp = requests.get(url, params=params)
    if resp.status_code == 200:
        data = resp.json()
        if data.get('data').get('status') == 'valid':
            return 'valid'
