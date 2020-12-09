from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='blog-home'),
	path('about/', views.about, name='blog-about'),
	path('folderview/<path:folderpath>',views.folderview,name='blog-folderview'),
	path('create/<path:folderpath>',views.create_file_in_folder,name='blog-create_file_in_folder'),
]
