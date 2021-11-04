"""abra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path


from MessageApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_app, name='login_app'),
    path('logout/', views.logout_view, name='logout_view'),
    path('getMessages/', views.get_messages, name='get_messages'),
    path('addMessage/', views.add_message, name='add_messages'),
    path('getUnreadMessages/', views.get_unread_messages, name='get_unread_messages'),
    path('readMessage/<int:message_id>', views.read_message, name='read_message'),
    path('deleteMessage/<int:message_id>/', views.delete_message, name='delete_message')
]
