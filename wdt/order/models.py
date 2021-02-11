import uuid

from django.db import models

from wdt.menu.models import Item


class Order(models.Model):
    class Meta:
        db_table = "order"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100)
    postcode = models.CharField(max_length=8)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.CharField(max_length=100)
    delivery_instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderItem(models.Model):
    """ Items in an order """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order_id", "item_id"],
                name="unique_order_and_item",
            ),
        ]
        db_table = "order_item"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.item.name}:{self.quantity}"
