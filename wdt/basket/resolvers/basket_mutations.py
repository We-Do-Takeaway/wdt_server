from ariadne import convert_kwargs_to_snake_case, ObjectType
from django.db import transaction

from wdt.basket.models import Basket, BasketItem
from wdt.menu.models import Item
from wdt.shared.exceptions import (
    InvalidBasketError,
    InvalidBasketOperation,
    InvalidItemError,
)

basket_mutation = ObjectType("Mutation")

INVALID_BASKET = "Invalid basket id"
INVALID_ITEM = "Invalid item id"
INVALID_QUANTITY = "Invalid quantity"
MAX_ITEMS_ALLOWED = 50


@basket_mutation.field("addBasketItem")
@convert_kwargs_to_snake_case
@transaction.atomic
def resolve_add_basket_item(obj, info, *, basket_id, basket_item):
    # Check if there is a basket to add to, if not then create it
    try:
        basket = Basket.objects.get(pk=basket_id)
    except Basket.DoesNotExist:
        basket = Basket(id=basket_id)
        basket.save()

    # Check that the item id refers toa real item
    try:
        Item.objects.get(pk=basket_item["item_id"])
    except Item.DoesNotExist:
        raise InvalidItemError(INVALID_ITEM)

    # If there is an entry for this item already then add this quantity to it
    # as the customer wants to add more
    try:
        db_basket_item = BasketItem.objects.get(
            item_id=basket_item["item_id"],
            basket_id=basket_id,
        )
        db_basket_item.quantity += basket_item["quantity"]
    except BasketItem.DoesNotExist:
        db_basket_item = BasketItem(
            basket_id=basket_id,
            item_id=basket_item["item_id"],
            quantity=basket_item["quantity"],
        )

    # The quantity passed in or the new quantity takes us over the max allowed
    if db_basket_item.quantity > MAX_ITEMS_ALLOWED or db_basket_item.quantity < 1:
        raise InvalidItemError(INVALID_QUANTITY)

    # All good, save to the db and return the new basket
    db_basket_item.save()
    return basket


@basket_mutation.field("updateBasketItem")
@convert_kwargs_to_snake_case
@transaction.atomic
def resolve_update_basket_item(obj, info, *, basket_id, basket_item):
    # Check the basket exists and fetch it for the response
    try:
        basket = Basket.objects.get(pk=basket_id)
    except Basket.DoesNotExist:
        raise InvalidBasketError(INVALID_BASKET)

    quantity = basket_item["quantity"]

    # Make sure we aren't trying to set an invalid quantity
    if quantity > 99 or quantity < 0:
        raise InvalidItemError(INVALID_QUANTITY)

    # The find the basket item entry to update
    try:
        db_basket_item = BasketItem.objects.get(
            item_id=basket_item["item_id"],
            basket_id=basket_id,
        )

        # We can only update the quantity so change that
        if quantity == 0:
            db_basket_item.delete()
        else:
            db_basket_item.quantity = quantity
            db_basket_item.save()

    # There is no entry with that combination of basket id and item
    # We know the basket exists so there's no item entry for it
    except BasketItem.DoesNotExist:
        raise InvalidBasketOperation(INVALID_ITEM)

    # All done, return the basket and let the type resolvers get the rest
    return basket


@basket_mutation.field("removeBasketItem")
@convert_kwargs_to_snake_case
@transaction.atomic
def resolve_remove_basket_item(obj, info, *, basket_id, item_id):
    # Check the basket exists and fetch it for the response
    try:
        basket = Basket.objects.get(pk=basket_id)
    except Basket.DoesNotExist:
        raise InvalidBasketError(INVALID_BASKET)

    try:
        BasketItem.objects.get(item_id=item_id, basket_id=basket_id).delete()
    except BasketItem.DoesNotExist:
        raise InvalidBasketOperation(INVALID_ITEM)

    return basket


@basket_mutation.field("clearBasket")
@convert_kwargs_to_snake_case
@transaction.atomic
def resolve_clear_basket(obj, info, *, basket_id):
    # Check the basket exists and fetch it for the response
    try:
        basket = Basket.objects.get(pk=basket_id)
        basket.basketitem_set.all().delete()
    except Basket.DoesNotExist:
        basket = Basket(id=id)
        basket.save()

    return basket
