from django.urls import path
from interface import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home')
]
