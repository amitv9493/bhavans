from . import client
from rest_framework.serializers import ValidationError
from rest_framework import status

class RazorpayClient:
    def create_order(self, registration_id, amount):
        
        try:
            razorpay_order = client.order.create(
                dict(
                    amount=amount * 100,
                    currency="INR",
                    receipt=str(registration_id),
                    payment_capture="0",
                )
            )
            return razorpay_order
        
        except Exception as e:
            raise ValidationError({"msg":e}, code = status.HTTP_400_BAD_REQUEST)

        # dict(amount=final_price*100, currency=currency, notes = notes, receipt=str(registration_id), payment_capture='0'
    
    def verify_payment(self, razorpay_payment_id, razorpay_order_id, razorpay_signature):
        try:
            x =  client.utility.verify_payment_signature({
                "razorpay_payment_id":razorpay_payment_id,
                "razorpay_order_id":razorpay_order_id,
                "razorpay_signature":razorpay_signature,
            })
            return x
            print(x)
            
        
        except Exception as e:
            raise ValidationError({"msg":e})
            
        