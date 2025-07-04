from django.db import models
from django.contrib.auth.models import User

class ExpenseIncome(models.Model):
    # Choices for transaction and tax types
    TRANSACTION_TYPES = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )
    TAX_TYPES = (
        ('flat', 'Flat'),
        ('percentage', 'Percentage'),
    )

    # Model fields
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User model
    title = models.CharField(max_length=200)  # Title of the transaction
    description = models.TextField(blank=True, null=True)  # Optional description
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Transaction amount
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)  # Credit or Debit
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Tax amount
    tax_type = models.CharField(max_length=10, choices=TAX_TYPES, default='flat')  # Flat or Percentage tax
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set creation time
    updated_at = models.DateTimeField(auto_now=True)  # Auto-set update time

    def calculate_total(self):
        """Calculate total amount including tax."""
        if self.tax_type == 'flat':
            return self.amount + self.tax  
        return self.amount + (self.amount * (self.tax / 100))  

    def __str__(self):
        """String representation of the model."""
        return f"{self.title} - {self.transaction_type}"