from django.shortcuts import render
from django.views.generic import ListView
from .models import Kakotora

# Create your views here.
class KakotoraListView(ListView):
    model = Kakotora
    template_name = 'kakotora/kakotora_list.html'
    context_object_name = 'kakotoras'
