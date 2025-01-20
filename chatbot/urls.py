from django.urls import path
from . import views

app_name = "chatbot"  # Define the namespace

urlpatterns = [
    path("", views.chatbot_home, name="chatbot_home"),
    path("send_message/", views.send_message, name="send_message"),
    path("user_details/", views.user_details, name="user_details"),
    path("ticket_details/", views.ticket_details, name="ticket_details"),
    path("payment/<int:booking_id>/", views.payment, name="payment"),
    path("success/", views.success, name="success"),    # Payment URL with booking_id
]
