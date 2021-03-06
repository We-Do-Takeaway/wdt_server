from ariadne import ObjectType

from wdt.basket.models import Basket

basket_query = ObjectType("Query")
basket_type = ObjectType("Basket")


@basket_query.field("basket")
def resolve_basket(obj, info, *, id):
    try:
        basket = Basket.objects.get(pk=id)
    except Basket.DoesNotExist:
        # Create an empty basket
        basket = Basket(id=id)
        basket.save()

    return basket


@basket_type.field("items")
def resolve_basket_items(basket, info):
    return basket.basketitem_set.all().order_by("item__name")
