from django.http import JsonResponse
from django.shortcuts import render, redirect
import requests
from .forms import UserDetailsForm
from .models import UserDetails, TicketBooking
from django.core.mail import send_mail
from django.conf import settings

# Rasa server endpoint
RASA_SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"


def chatbot_home(request):
    """
    Renders the chatbot interface with the conversation history from the session.
    """
    conversation_history = request.session.get('conversation_history', [])
    return render(request, "chatbot/chatbot.html", {"conversation_history": conversation_history})


def send_message(request):
    """
    Sends the user message to Rasa and retrieves the bot's response.
    Updates the conversation history in the session.
    """
    if request.method == "POST":
        user_message = request.POST.get("message")
        payload = {"sender": "user", "message": user_message}
        response = requests.post(RASA_SERVER_URL, json=payload)
        bot_responses = [msg["text"] for msg in response.json()]

        conversation_history = request.session.get('conversation_history', [])
        conversation_history.append({'user': user_message, 'bot': bot_responses})
        request.session['conversation_history'] = conversation_history

        return JsonResponse({"messages": bot_responses})
    return JsonResponse({"error": "Invalid request"}, status=400)


def user_details(request):
    """
    Handles user details form submission and stores ticket details in the session.
    Redirects to the ticket details page after saving data.
    """
    if request.method == "POST":
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            user_details = UserDetails.objects.create(
                name=form.cleaned_data['name'],
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                email=form.cleaned_data['email']
            )

            ticket_count = request.GET.get('ticket_count', 0)
            ticket_type = request.GET.get('ticket_type', 'general')
            ticket_price = 200
            total_price = int(ticket_count) * ticket_price

            request.session['ticket_details'] = {
                'ticket_count': ticket_count,
                'ticket_type': ticket_type,
                'total_price': total_price,
                'email': form.cleaned_data['email']  # Save email in session for later use
            }

            return redirect('chatbot:ticket_details')
    else:
        form = UserDetailsForm()
    return render(request, "chatbot/user_details.html", {"form": form})


def ticket_details(request):
    """
    Retrieves ticket details from the session and saves the booking to the database.
    Sends a confirmation email to the user.
    """
    ticket_details = request.session.get('ticket_details', {})
    ticket_count = ticket_details.get('ticket_count', 0)
    ticket_type = ticket_details.get('ticket_type', 'general')
    total_price = ticket_details.get('total_price', 0)
    user_email = ticket_details.get('email')

    booking = TicketBooking.objects.create(
        ticket_count=ticket_count,
        ticket_type=ticket_type,
        total_price=total_price,
        payment_method=None,
        payment_status="Pending"
    )

    send_booking_confirmation(booking, user_email)

    return render(request, "chatbot/ticket_details.html", {
        "ticket_count": ticket_count,
        "ticket_type": ticket_type.capitalize(),
        "total_price": total_price,
        "booking_id": booking.id,
    })


def payment(request, booking_id):
    """
    Handles payment processing. Updates booking with payment method and status.
    Redirects to the success page after processing payment.
    """
    booking = TicketBooking.objects.get(id=booking_id)

    if request.method == "POST":
        payment_method = request.POST.get('payment_method', 'Credit Card')
        booking.payment_method = payment_method
        booking.payment_status = "Completed"
        booking.save()

        return redirect("/chatbot/success/")

    return render(request, "chatbot/payment.html", {"booking": booking})


def success(request):
    """
    Handles the success page after booking. Adds a success message to the conversation history.
    """
    conversation_history = request.session.get('conversation_history', [])
    success_message = "Your booking was successful! A confirmation email with your booking details has been sent to your email."
    conversation_history.append({'user': 'booking_success', 'bot': success_message})
    request.session['conversation_history'] = conversation_history

    return render(request, "chatbot/success.html", {"conversation_history": conversation_history})


def send_booking_confirmation(booking, user_email):
    """
    Sends a booking confirmation email to the user.
    """
    subject = "Booking Confirmation"
    message = (
        f"Your booking was successful!\n\n"
        f"Booking Details:\n"
        f"Ticket Count: {booking.ticket_count}\n"
        f"Ticket Type: {booking.ticket_type.capitalize()}\n"
        f"Total Price: {booking.total_price}\n"
    )
    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])