from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from .models import Client, Broadcast, Message
from .serializers import ClientSerializer, BroadcastSerializer, MessageSerializer
from .tasks import send_broadcast
from django.utils import timezone
from rest_framework.decorators import api_view

class ClientListCreate(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ClientRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class BroadcastListCreate(generics.ListCreateAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer

    def perform_create(self, serializer):
        broadcast = serializer.save()
        if broadcast.start_datetime <= timezone.now():
            send_broadcast.delay(broadcast.id)
        else:
            send_broadcast.apply_async((broadcast.id,), eta=broadcast.start_datetime)

class BroadcastRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Broadcast.objects.all()
    serializer_class = BroadcastSerializer

    def perform_update(self, serializer):
        broadcast = serializer.save()
        if broadcast.start_datetime <= timezone.now() <= broadcast.end_datetime:
            send_broadcast.delay(broadcast.id)

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


class BroadcastStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        statistics = Broadcast.objects.annotate(
            messages_sent=Count('message'),
            messages_by_status=Count('message__sending_status')
        ).values('id', 'start_datetime', 'end_datetime', 'messages_sent', 'messages_by_status')
        return Response(statistics)

class BroadcastDetailStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        broadcast_id = kwargs.get('pk')
        statistics = Message.objects.filter(broadcast_id=broadcast_id).values('sending_status').annotate(count=Count('id'))
        return Response(statistics)


@api_view(['POST'])
def start_broadcast(request, pk):
    try:
        broadcast = Broadcast.objects.get(pk=pk, end_datetime__gt=timezone.now())
        send_broadcast.delay(broadcast.id)
        return Response({'status': 'Broadcast started'}, status=status.HTTP_200_OK)
    except Broadcast.DoesNotExist:
        return Response({'error': 'Broadcast not found or already ended'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def stop_broadcast(request, pk):
    return Response({'status': 'Broadcast stopped'}, status=status.HTTP_200_OK)
