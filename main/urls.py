from  django.urls import path
from . import views

app_name = 'main'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('document/list/', views.DocumentListView.as_view(), name='document_list'),
    path('document/<int:pk>/detail/', views.DocumentDetailView.as_view(), name='document_detail'),
    path('document/create/', views.DocumentCreateView.as_view(), name='document_create'),


    path('document/<int:file_id>/view/', views.view_file, name='view_file'),
    path('document/<int:file_id>/download/', views.download_file, name='download_file'),
]
