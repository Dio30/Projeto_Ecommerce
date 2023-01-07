from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from django.dispatch import receiver


@receiver(valid_ipn_received)
def valid_ipn_signal(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == "COMPLETED":
        pass
    
@receiver(invalid_ipn_received)
def invalid_ipn_signal(sender, **kwargs):
    ipn = sender
    if ipn.payment_status == "COMPLETED":
      pass