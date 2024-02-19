import requests

class HaApi:
    def __init__(self, url: str, token: str, timeout: float = 1.0, logging = False):
        self.base_url = url
        self.token = token
        self.timeout = timeout
        self.logging = logging

        self.headers = {
            "Authorization": f'Bearer {token}',
            "content-type": "application/json",
        }

    def log(self, *args):
        if self.logging: print(*args)

    def turn_on(self, data: object, id = None):
        url = self.base_url + '/services/light/turn_on'

        try:
            response = requests.post(url, json=data, headers=self.headers, timeout=self.timeout)

            if not response.ok:
                error_message = response.json()
                raise ValueError(f'HTTP Error: {error_message}')
            
            self.log(id, "Sent", data)

            return response.json()
        except requests.exceptions.ReadTimeout:
            self.log(id, "Timed out")
    