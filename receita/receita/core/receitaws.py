import requests
from django.conf import settings

RECEITA_WS_API_TOKEN = settings.RECEITA_WS_API_TOKEN


class ReceitaWS:
    def __init__(self, token=RECEITA_WS_API_TOKEN):
        self.token = token
        self.base_url = "https://receitaws.com.br/v1"
    
    def get_from_cnpj(self, cnpj):
        url = f"{self.base_url}/cnpj/{cnpj}/"
        headers = {"Authentication": f"Bearer {self.token}"}
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data.get('status') == 'ERROR':
            raise requests.HTTPError(data['message'])
        return response.json()
