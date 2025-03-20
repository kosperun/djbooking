import stripe
from django.conf import settings
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from payments.tasks import confirm_payment


class StripeWebhooksAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        event = None

        try:
            event = stripe.Webhook.construct_event(
                request.body, request.META["HTTP_STRIPE_SIGNATURE"], settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError as e:
            # Invalid payload
            print("Error parsing payload: {}".format(str(e)))
            return Response(status=HTTP_400_BAD_REQUEST)
        except stripe.SignatureVerificationError as e:
            # Invalid signature
            print("Error verifying webhook signature: {}".format(str(e)))
            return Response(status=HTTP_400_BAD_REQUEST)

        # Handle the event
        if event.type == "payment_intent.succeeded":
            payment_intent = event.data.object
            confirm_payment.delay(payment_intent)

        return Response(status=HTTP_200_OK)
