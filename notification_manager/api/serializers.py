from rest_framework import serializers
from .models import Client, Broadcast, Message

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone_number', 'mobile_operator_code', 'tag', 'timezone']

class BroadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broadcast
        fields = ['id', 'start_datetime', 'message_text', 'client_properties_filter', 'end_datetime']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'creation_datetime', 'sending_status', 'broadcast', 'client']
