from django.db import models


class Item(models.Model):
    """Модель для товара."""
    CURRENCY_CHOICES = [
        ('usd', 'USD'),
        ('rub', 'RUB'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='usd')

    def __str__(self):
        return f"Item {self.name}"


class Discount(models.Model):
    """Модель для скидки."""
    coupon_id = models.CharField(max_length=255, unique=True)
    percent_off = models.FloatField()
    duration = models.CharField(max_length=50)

    def __str__(self):
        return f"Discount {self.coupon_id} ({self.percent_off}%)"


class Tax(models.Model):
    """Модель для налога."""
    tax_id = models.CharField(max_length=255, unique=True)
    display_name = models.CharField(max_length=255)
    percentage = models.FloatField()
    inclusive = models.BooleanField(default=False)

    def __str__(self):
        return f"Tax {self.display_name} ({self.percentage}%)"


class Order(models.Model):
    """Модель для группы товаров."""
    id = models.BigAutoField(primary_key=True)
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order {self.id}"
