from django.db import models

# Create your models here.
from django.db import models

class Transaction(models.Model):
    short_code = models.CharField(max_length=100)
    msisdn = models.CharField(max_length=15)  # The customer's phone number
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bill_ref_number = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=100, default='Pending')  

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.amount} KES"
