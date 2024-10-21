from django.urls import path
from .views import (DashboardView, AllPageView, WaitingPageView, AcceptedPageView,
                    CancelledPageView, DocumentDetailView, ReceiveDocumentView)

app_name = "receiver"
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('all/', AllPageView.as_view(), name='all'),
    path('waiting/', WaitingPageView.as_view(), name='waiting'),
    path('accepted/', AcceptedPageView.as_view(), name='accepted'),
    path('cancelled/', CancelledPageView.as_view(), name='cancelled'),
    path('<int:pk>/detail/', DocumentDetailView.as_view(), name='detail'),
    path('<int:pk>/receive/', ReceiveDocumentView.as_view(), name='receive'),
]