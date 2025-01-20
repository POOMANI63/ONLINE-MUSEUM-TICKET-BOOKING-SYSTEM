from django.db import models

class UserDetails(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} ({self.email})"

class TicketBooking(models.Model):
    # Fields for storing ticket details
    ticket_count = models.IntegerField()
    ticket_type = models.CharField(max_length=20)  # e.g., 'adult', 'children', etc.
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Fields for storing payment method
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    payment_status = models.CharField(max_length=20, default="Pending")  # 'Pending', 'Completed', etc.
    
    # Optional: Timestamp for when the booking was made
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Booking - {self.ticket_count} {self.ticket_type} tickets for ₹{self.total_price}"
