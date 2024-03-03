from django.urls import path
from .views import (ClientListCreate, ClientRetrieveUpdateDestroy, BroadcastListCreate, BroadcastRetrieveUpdateDestroy,
                    BroadcastStatisticsView, BroadcastDetailStatisticsView,
                    start_broadcast, stop_broadcast)
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Notification Manager API",
      default_version='v1',
      description="API documentation for notification manager",
      contact=openapi.Contact(email="mbuhtiarovlinked@gmail.com")
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('clients/', ClientListCreate.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', ClientRetrieveUpdateDestroy.as_view(), name='client-detail'),
    path('broadcasts/', BroadcastListCreate.as_view(), name='broadcast-list-create'),
    path('broadcasts/<int:pk>/', BroadcastRetrieveUpdateDestroy.as_view(), name='broadcast-detail'),
    path('broadcasts/<int:pk>/start/', start_broadcast, name='broadcast-start'),
    path('broadcasts/<int:pk>/stop/', stop_broadcast, name='broadcast-stop'),
    path('broadcasts/statistics/', BroadcastStatisticsView.as_view(), name='broadcast-statistics'),
    path('broadcasts/<int:pk>/statistics/', BroadcastDetailStatisticsView.as_view(), name='broadcast-detail-statistics'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
