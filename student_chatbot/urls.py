from django.contrib import admin
from django.urls import path, include
from chatbot_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.custom_login, name='login'),
    path('admin/logout/', views.custom_logout, name='admin-logout'),  # custom admin logout
    path('', include('chatbot_app.urls')),
]
