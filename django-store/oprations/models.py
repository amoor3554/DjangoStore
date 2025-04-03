from django.db import models
from django.utils.translation import gettext as trans


class TransactionsStatus(models.IntegerChoices):
    PENDING = 0, trans('Pending')
    COMPLETED = 1, trans('Completed')


class PaymentMethod(models.IntegerChoices):
    PAYPAL = 1, trans('PayPal')
    STRIPE = 2, trans('Stripe')


class Transaction(models.Model):
    session = models.CharField(max_length=255)
    items = models.JSONField(default=dict)
    customer = models.JSONField(default=dict)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.IntegerField(choices=TransactionsStatus.choices, default=TransactionsStatus.PENDING)
    payment_method = models.IntegerField(choices=PaymentMethod.choices, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def customer_name(self):
        return self.customer['first_name'] + ' ' + self.customer['last_name']
    
    @property
    def customer_email(self):
        return self.customer['email']



