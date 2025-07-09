from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update-profile/', views.update_profile, name='update-profile'),
    path('chatbot/', views.chat, name='chat'),
]
