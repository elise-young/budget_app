import requests
import json

#basically a fake front end

def GetSummary():
    transactions = requests.get('http://127.0.0.1:8000/transactions').json()
    total_inflow = 0
    total_outflow = 0
    for transaction in transactions:
        total_inflow = total_inflow + int(transaction['inflow'])
        total_outflow = total_outflow + int(transaction['outflow'])
    available = total_inflow - total_outflow

    categories = requests.get('http://127.0.0.1:8000/categories').json()

    return({'available' : available, 'categories':categories})

