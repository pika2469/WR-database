from django.urls import path
from . import views

urlpatterns = [
    path('', views.KakotoraListView.as_view(), name='kakotora_list'),
]
