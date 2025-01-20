from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
import re

class ActionBookTicket(Action):
    def name(self):
        return "action_book_ticket"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        # Extract slots
        time = tracker.get_slot("time")
        tickets = tracker.get_slot("number_of_tickets")
        ticket_type = tracker.get_slot("ticket_type") or "unspecified"

        # Validate time input
        time_formats = ['%I:%M %p', '%I %p', '%H:%M']  # Common time formats
        time_obj = None

        if time:
            time = time.lower().strip()
            time = re.sub(r'(\d)(am|pm)', r'\1 \2', time)  # Add space before AM/PM if missing
            time = re.sub(r'(\d+):?(\d*)(am|pm)', r'\1:\2 \3', time)  # Normalize to "HH:MM AM/PM"
            for fmt in time_formats:
                try:
                    time_obj = datetime.strptime(time, fmt)
                    break
                except ValueError:
                    continue

        if not time_obj:
            dispatcher.utter_message(text="Please provide the time in a valid format, e.g., 'i want to book 2 adults tickets for 3:00 PM'.")
            return []

        # Check if time is valid
        if time_obj.hour < 10 or time_obj.hour >= 17:
            dispatcher.utter_message(text="The museum only operates between 10:00 AM and 5:00 PM. Please enter a time within this range.")
            return []

        formatted_time = time_obj.strftime('%I:%M %p')  # Ensure correct time formatting

        # Validate ticket count
        tickets_count = None
        if tickets:
            try:
                tickets_count = int(re.search(r'\d+', tickets).group())
            except (ValueError, AttributeError):
                dispatcher.utter_message(text="Please specify a valid number of tickets.")
                return []

        if not tickets_count or tickets_count <= 0:
            dispatcher.utter_message(text="The number of tickets must be greater than zero.")
            return []

        # Determine ticket type
        ticket_type = (
            "adult" if "adult" in ticket_type.lower() else
            "children" if "children" in ticket_type.lower() else
            "general"
        )

        # Calculate ticket price
        ticket_price = 200  # Default price for adult tickets
        if ticket_type == "children":
            ticket_price = 100
        elif ticket_type == "senior":
            ticket_price = 200

        total_amount = ticket_price * tickets_count

        # Generate the link dynamically with the ticket details and price
        link = f"http://127.0.0.1:8000/chatbot/user_details/?ticket_count={tickets_count}&ticket_type={ticket_type}&total_amount={total_amount}"

        # Send the message with the clickable link
        dispatcher.utter_message(
            text=f"Your {tickets_count} {ticket_type} ticket(s) for {formatted_time} have been successfully booked! "
                 f"The total amount is ₹{total_amount}. Please ({link}) to provide your details and proceed with payment."
        )

        # Alternatively, send buttons if needed
        buttons = [
            {
                "title": "Proceed to Payment",
                "payload": f"/proceed_payment{{'ticket_count': {tickets_count}, 'ticket_type': '{ticket_type}', 'total_amount': {total_amount}}}"
            }
        ]
        dispatcher.utter_message(text="Click below to proceed with payment:", buttons=buttons)

        # Set booking status as confirmed
        return [SlotSet("booking_status", "confirmed")]






class ActionFallbackCustom(Action):
    def name(self):
        return "action_custom_fallback"

    def run(self, dispatcher: CollectingDispatcher, tracker, domain):
        dispatcher.utter_message(
            text="I'm sorry, I didn't understand that. Can you rephrase?"
        )
        return []
