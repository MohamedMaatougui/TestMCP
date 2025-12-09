from .views import *
from django.urls import path

urlpatterns = [
    path('',simple_view, name='conference_simple_view'),    #url,fonction ou classe, nom de la route
    path('home/',home_view,name='conference_home'),
    path('welcome/<str:name>/', welcome, name='conference_welcome'),
    path('list/',listConferences,name='conference_list'),
    path('listC/',ConferenceListView.as_view(),name='conference_list_view'),
    path('details/<int:pk>',ConferenceDetailView.as_view(),name='conference_details_view'),
    path('add/',ConferenceCreateView.as_view(),name = 'conference_create_view'),
    path('update/<int:pk>',ConferenceUpdateView.as_view(),name = 'conference_update_view'),
    path('delete/<int:pk>',ConferenceDeleteView.as_view(),name = 'conference_delete_view'),
]

