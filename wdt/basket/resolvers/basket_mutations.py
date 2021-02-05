from ariadne import ObjectType, convert_kwargs_to_snake_case

from wdt.basket.models import Basket, BasketItem

basket_mutation = ObjectType("Mutation")


@basket_mutation.field("addBasketItem")
@convert_kwargs_to_snake_case
def resolve_add_basket_item(obj, info, *, basket_id, basket_item):
    # Check if there is a basket to add to, if not then remove it
    try:
        basket = Basket.objects.get(pk=basket_id)
    except Basket.DoesNotExist:
        basket = Basket(id=basket_id)
        basket.save()

    basket_item = BasketItem(
        basket_id=basket_id,
        item_id=basket_item["item_id"],
        quantity=basket_item["quantity"],
    )

    basket_item.save()

    return basket


@basket_mutation.field("updateBasketItem")
@convert_kwargs_to_snake_case
def resolve_update_basket_item(obj, info, *, basket_id, basket_item):
    # Check if there is a basket to add to, if not then remove it
    try:
        basket = Basket.objects.get(pk=basket_id)
        old_item = BasketItem.objects.get(item_id=basket_item.item_id)
        old_item.delete()
    except Basket.DoesNotExist:
        return None
    except BasketItem.DoesNotExist:
        return None

    item = BasketItem(
        item_id=basket_item["item_id"],
        quantity=basket_item["quantity"],
    )

    item.save()

    return basket


@basket_mutation.field("removeBasketItem")
@convert_kwargs_to_snake_case
def resolve_remove_basket_item(obj, info, *, basket_id, item_id):
    # Delete the item then fetch the basket
    try:
        old_item = BasketItem.objects.get(item_id=item_id, basket_id=basket_id)
        old_item.delete()
        basket = Basket.objects.get(pk=basket_id)
    except Basket.DoesNotExist:
        return None

    return basket


@basket_mutation.field("clearBasket")
@convert_kwargs_to_snake_case
def resolve_clear_basket(obj, info, *, basket_id):
    # Check if there is a basket to add to, if not then remove it
    try:
        basket = Basket.objects.get(pk=basket_id)
    except Basket.DoesNotExist:
        return None

    basket.basketitem_set.all().delete()

    return basket
