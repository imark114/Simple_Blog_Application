from django.urls import path
from . import views

urlpatterns = [
    path('register_user/', views.RgisterUserApiView.as_view(), name='register_user'),
    path('user_profile/', views.UserProfileApiView.as_view(), name='user_profile'),
    path('blogs/', views.BlogApiView.as_view(), name='blogs'),
    path('blogs/<int:pk>/', views.BlogApiView.as_view(), name='blogs'),
    path('blogs_list/', views.AllBlogApiView.as_view(), name='all_blogs'),
]
