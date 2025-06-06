from django.db import models

# Create your models here.
class Item(models.Model):
    def __str__(self):
        return self.item_name

    item_name=models.CharField(max_length=300)
    item_desc=models.CharField(max_length=400)
    item_price=models.FloatField()

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"

class Payment(models.Model):
    ORDER_STATUS_CHOICES=[
        ('created','Created'),
        ('paid','Paid'),
        ('failed','Failed')
    ]

    #Razorpay API fields
    order_id=models.CharField(max_length=200,unique=True)
    payment_id=models.CharField(max_length=200,blank=True,null=True)
    amount=models.IntegerField(help_text="Amount in paise ex:Rs 50 = 5000")
    status=models.CharField(max_length=200, choices=ORDER_STATUS_CHOICES, default='created')


    # Guest customer delivery info
    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - ₹{self.amount / 100:.2f} - {self.status}"