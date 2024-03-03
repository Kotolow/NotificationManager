# tasks.py

from celery import shared_task
from .models import Broadcast, Client, Message
from django.utils import timezone
import requests


@shared_task
def send_broadcast(broadcast_id):
    broadcast = Broadcast.objects.get(id=broadcast_id)
    if broadcast.start_datetime <= timezone.now() <= broadcast.end_datetime:
        clients = Client.objects.filter(**broadcast.client_properties_filter)
        for client in clients:
            send_message.delay(broadcast.message_text, client.phone_number)


@shared_task
def send_message(message_text, phone_number, broadcast_id, client_id):
    url = 'https://probe.fbrq.cloud/v1/send/'
    headers = {'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3Mzk4ODU0MTQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6IkBLb3RvbG93In0.gBT9z9cz9JbGMf8NptVqL5Qvnr54vqS9UyYibCdCbME'}
    data = {'phone': phone_number, 'text': message_text}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        sending_status = 'SENT' if response.status_code == 200 else 'FAILED'
    except requests.exceptions.RequestException as e:
        sending_status = 'ERROR'

    Message.objects.create(
        sending_status=sending_status,
        broadcast_id=broadcast_id,
        client_id=client_id
    )
