from django.urls import path
from .views import *


urlpatterns = [
    path('item/<int:id>/', item_detail, name='item_detail'),
    path('order/<int:id>/', order_detail, name='order_detail'),
    path('buy/<int:id>/', create_checkout_session, name='create_checkout_session'),
    path('buy_order/<int:order_id>/', create_checkout_session_for_order, name='create_checkout_session_for_order'),
    path('create-payment-intent/<int:id>/', create_payment_intent, name='create_payment_intent'),
    path('success/', payment_success, name='payment_success'),
]
