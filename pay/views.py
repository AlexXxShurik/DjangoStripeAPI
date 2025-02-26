import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Item, Order


def create_checkout_session(request, id):
    item = get_object_or_404(Item, id=id)

    # Выбираем ключи Stripe в зависимости от валюты товара
    stripe_keys = settings.STRIPE_KEYS[item.currency]
    stripe.api_key = stripe_keys['secret_key']

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": item.currency,
                    "product_data": {"name": item.name},
                    "unit_amount": item.price * 100,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=settings.URL + "/success/",
        cancel_url=settings.URL + "/cancel/",
    )

    return JsonResponse({"session_id": session.id})


def create_payment_intent(request, id):
    item = get_object_or_404(Item, id=id)

    stripe_keys = settings.STRIPE_KEYS[item.currency]
    stripe.api_key = stripe_keys['secret_key']

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(item.price * 100),
            currency=item.currency,
            payment_method_types=["card"],
            description=f"Payment for {item.name}",
            metadata={"item_id": item.id},
        )
        return JsonResponse({"client_secret": intent.client_secret})
    except stripe.error.StripeError as e:
        return JsonResponse({"error": str(e)}, status=400)


def payment_success(request):
    return render(request, "pay/success.html")


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    stripe_public_key = settings.STRIPE_KEYS[item.currency]['public_key']
    return render(request, "pay/item.html", {
        "item": item,
        "stripe_public_key": stripe_public_key,
    })


def create_checkout_session_for_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    stripe_keys = settings.STRIPE_KEYS['usd']
    stripe.api_key = stripe_keys['secret_key']

    line_items = [
        {
            "price_data": {
                "currency": 'usd',
                "product_data": {"name": item.name},
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
            "tax_rates": [order.tax.tax_id] if order.tax and not order.tax.inclusive else [],
        }
        for item in order.items.all()
    ]

    discounts = []
    if order.discount:
        discounts.append({"coupon": order.discount.coupon_id})

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        discounts=discounts,
        success_url=settings.URL + "/success/",
        cancel_url=settings.URL + "/cancel/",
    )

    return JsonResponse({"session_id": session.id})


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)

    stripe_public_key = settings.STRIPE_KEYS['usd']['public_key']

    subtotal = sum(item.price for item in order.items.all())

    discount_amount = 0
    if order.discount:
        discount_amount = subtotal * (order.discount.percent_off / 100)

    tax_amount = 0
    if order.tax and not order.tax.inclusive:
        tax_amount = (subtotal - discount_amount) * (order.tax.percentage / 100)

    total_price = subtotal - discount_amount + tax_amount

    subtotal = round(subtotal, 2)
    discount_amount = round(discount_amount, 2)
    tax_amount = round(tax_amount, 2)
    total_price = round(total_price, 2)

    return render(request, "pay/order.html", {
        "order": order,
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "tax_amount": tax_amount,
        "total_price": total_price,
        "stripe_public_key": stripe_public_key,
    })
