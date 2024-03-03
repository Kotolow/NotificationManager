from django.db import models

class Client(models.Model):
    id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=11)
    mobile_operator_code = models.IntegerField()
    tag = models.CharField(max_length=255)
    timezone = models.CharField(max_length=255)

class Broadcast(models.Model):
    id = models.AutoField(primary_key=True)
    start_datetime = models.DateTimeField()
    message_text = models.TextField()
    client_properties_filter = models.JSONField()
    end_datetime = models.DateTimeField()

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    sending_status = models.CharField(max_length=255)
    broadcast = models.ForeignKey(Broadcast, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)