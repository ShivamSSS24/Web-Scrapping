from celery import shared_task
import requests
from .models import Job, Task
from django.utils import timezone

COINMARKETCAP_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
API_KEY = 'your_coinmarketcap_api_key'

@shared_task
def fetch_coin_data(job_id, coin):
    job = Job.objects.get(id=job_id)
    task = Task.objects.create(job=job, coin=coin)

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }
    params = {
        'symbol': coin,
        'convert': 'USD'
    }

    response = requests.get(COINMARKETCAP_API_URL, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200:
        task.status = 'completed'
        task.result = data
        task.completed_at = timezone.now()
    else:
        task.status = 'failed'
        task.result = data.get('status', {}).get('error_message', 'Unknown error')
        task.completed_at = timezone.now()
    
    task.save()

@shared_task
def start_scraping(coins):
    job = Job.objects.create()
    for coin in coins:
        fetch_coin_data.delay(job.id, coin)
    return job.id
