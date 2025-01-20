# project_name/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chatbot/", include("chatbot.urls")),  # Including the chatbot app URLs
]
