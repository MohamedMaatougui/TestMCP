# SessionApp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path('<int:pk>/', views.session_detail, name='session_detail'),
    path('create/', views.session_create, name='session_create'),
    path('<int:pk>/update/', views.session_update, name='session_update'),
    path('<int:pk>/delete/', views.session_delete, name='session_delete'),
]
