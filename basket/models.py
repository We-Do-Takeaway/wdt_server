import uuid
from django.db import models

from menu.models import Item


class Basket(models.Model):
    class Meta:
        db_table = "basket"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    owner_id = models.UUIDField(editable=True)


class BasketItem(models.Model):
    """ Items in a basket """

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["basket_id", "item_id"],
                name="unique_basket_and_item"
            )
        ]
        db_table = "basket_item"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f'{self.item.name}:{self.quantity}'
