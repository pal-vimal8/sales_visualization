from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sales-performance/', views.sales_performance, name='sales_performance'),
    path('file-upload/', views.file_upload, name='file_upload'),
]
