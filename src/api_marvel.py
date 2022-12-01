import os
import requests
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class ApiMarvel:
    def __init__(self):
        self.hash = os.getenv('HASH')
        self.md5_hash = os.getenv('MD5HASH')
        self.apikey = os.getenv('APIKEY')
        self.headers = {self.hash: self.hash}
        self.endpoint = "https://gateway.marvel.com:443/v1/public"
        return None

    def get_data(self, n_offset, n_limit, type):
        url = f"{self.endpoint}/{type}?ts=1669338936&apikey={self.apikey}&hash={self.md5_hash}&offset={n_offset}&limit={n_limit}"

        payload = {}
        files = {}

        response = requests.request("GET", url, headers=self.headers, data=payload, files=files)

        return response

    def api_indicate_error(self):
        logging.critical(f"an error has occurred in conection, check API MARVEL in")
    def check_status_api(self, type):
        response = self.get_data(0, 1, type)
        data = json.loads(response.text)
        total = data['data']['total']
        if total == 0:
            return False
        return total

