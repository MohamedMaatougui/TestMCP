"""
URL configuration for firstProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from UserApp.views import RegisterView
from rest_framework.routers import DefaultRouter
from ConferenceApp import views
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView,)

router = DefaultRouter()
router.register(r'conferences', views.ConferenceViewSet)

urlpatterns = [
    path('API/', include(router.urls)),
    path('register/',RegisterView.as_view(), name='inscription'),
    path('logout/',auth_views.LogoutView.as_view(), name='logout'),
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path("", TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('conference/', include('ConferenceApp.urls')),
    path('session/', include('SessionApp.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
