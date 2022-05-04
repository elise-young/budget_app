import requests
import json

transactions = requests.get('http://127.0.0.1:8000/transactions').json()

