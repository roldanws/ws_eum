from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views


core_patterns = ([
    path('hom/', views.Home.as_view(), name='home'),
    path('upload/', views.upload, name='upload'),
    path('video/', views.video_list, name='video_list'),
    path('video/upload/', views.upload_video, name='upload_video'),
    path('videos/<int:pk>/', views.delete_video, name='delete_video'),

    path('videos/', views.VideoListView.as_view(), name='class_video_list'),
    path('class/videos/upload/', views.UploadVideoView.as_view(), name='class_upload_video'),

],"core")
