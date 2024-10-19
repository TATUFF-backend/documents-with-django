from django.urls import path
from .views import DashboardView, AllPageView


app_name = "receiver"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('all/', AllPageView.as_view(), name='all'),
]