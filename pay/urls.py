from django.urls import path
from .views import create_checkout_session, item_detail, create_checkout_session_for_order, order_detail

urlpatterns = [
    path('buy/<int:id>/', create_checkout_session, name="buy"),
    path('item/<int:id>/', item_detail, name="item_detail"),
    path('buy_order/<int:order_id>/', create_checkout_session_for_order, name='pay_order'),
    path('order/<int:id>/', order_detail, name="order_detail"),
]
