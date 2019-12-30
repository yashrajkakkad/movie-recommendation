from django.urls import path
from . import views
from .models import Node

urlpatterns = [
    path('', views.home, name='home'),
    path('autocomplete/', views.NodeAutocomplete.as_view(model=Node), name="autocomplete"),
    path('refresh/', views.refreshnodes, name="refresh"),
]
