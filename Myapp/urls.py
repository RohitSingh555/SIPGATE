from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('call-logs/', views.fetch_history, name='call_logs'),
    path('logs/', views.Logs, name='logs'),
    path('outgoing-call/', views.outgoing_call, name='outgoing_call'),
    path('on-hangup/', views.on_hangup, name='on_hangup'),
    path('incoming-call/', views.incoming_call, name='incoming_call'),
    # path('check-incoming-call/', views.check_incoming_call, name='check_incoming_call'),
]