from ariadne import ObjectType

from wdt.order.models import Order
from wdt.shared.exceptions import InvalidOrderError

order_query = ObjectType("Query")
order_type = ObjectType("Order")


@order_query.field("order")
def resolve_basket(obj, info, *, id):
    try:
        return Order.objects.get(pk=id)
    except Order.DoesNotExist:
        raise InvalidOrderError("Invalid order id")


@order_type.field("items")
def resolve_order_items(order, info):
    return order.orderitem_set.all().order_by("item__name")


@order_type.field("address1")
def resolve_address1(order, info):
    return order.address_1


@order_type.field("address2")
def resolve_address2(order, info):
    return order.address_2


@order_type.field("deliveryInstructions")
def resolve_delivery_instructions(order, info):
    return order.delivery_instructions


@order_type.field("createdAt")
def resolve_created_at(order, info):
    return order.created_at
