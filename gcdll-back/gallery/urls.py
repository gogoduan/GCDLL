"""TEST URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from gallery import views
from django.urls import include

urlpatterns = [
    path("search", views.search),  # 搜索，共通部分
    path("login", views.log_in),  # 游客与管理员登录
    path("home", views.tourist_home),  # 游客主页，显示所有展览
    path("exhibit", views.exhibit_info),  # 获取展览信息，点赞评论展览
    path("photo", views.photo_info),  # 获取照片信息，点赞评论照片
    path("comment", views.comment_info),  # 获取评论信息，点赞评论
    path("repair", views.repair_info),  # 获取修复中的照片集
    path("user", views.user_info),  # 获取用户信息
    path("fixupload", views.fixupload_photos),  # 照片修复页
    path("photoadmin", views.photo_admin),  # 照片管理
    path("galleryadmin", views.gallery_admin),  # 展览管理
    path("newgallery", views.setnew_gallery),  # 新建展览
    path("admintourist", views.admin_tourist),  # 管理游客
    path("exhibit_edit", views.edit_gallery),  # 增减图片
    path("admincomment", views.admin_comment),  # 管理评论
]
