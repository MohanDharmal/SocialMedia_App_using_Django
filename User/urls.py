"""
URL configuration for SocialMedia project.

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
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home,name='HomePage'),
    path('signup/',views.signup,name='signup'),
    path('loginn/',views.loginn,name='login'),
    path('logoutt/',views.logoutt,name='logoutt'),
    path('upload',views.upload),
    path('explore/',views.explore,name='explore'),
    path('profile/<str:username>/',views.profile,name='profile'),
    path('like-post/<str:id>/',views.likes,name='likes'),
    path('follow/',views.follow,name='follow'),
    path('delete/<str:id>/',views.delete,name='delete'),
    path('search-result/',views.search_result,name='search'),
    path('#<str:id>', views.home_post),
    path('post/<uuid:post_id>/', views.post_detail, name='post_detail'),
    path('send-message/<str:receiver_username>',views.send_message,name='send_message'),    
    path('message/',views.user_messages,name='user_messages'),    
]
