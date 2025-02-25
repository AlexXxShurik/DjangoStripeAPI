import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse

from .models import Item

stripe.api_key = settings.STRIPE_API_KEY
url = settings.URL


def create_checkout_session(request, id):
    item = get_object_or_404(Item, id=id)

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item.name},
                    "unit_amount": item.price * 100, # цена в центах, перевожу в $
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=url + "/success/",
        cancel_url=url + "/cancel/",
    )

    return JsonResponse({"session_id": session.id})


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    return render(request, "pay/item.html", {"item": item, "stripe_public_key": settings.STRIPE_PUBLIC_KEY})
