from ariadne import convert_kwargs_to_snake_case, ObjectType
from django.db import transaction

from wdt.menu.models import Item
from wdt.order.models import Order, OrderItem
from wdt.shared.exceptions import InvalidItemError, InvalidOrderOperation

order_mutation = ObjectType("Mutation")


@order_mutation.field("addOrder")
@convert_kwargs_to_snake_case
@transaction.atomic
def resolve_add_order(obj, info, *, order):
    # Check there are 1 or more items in the order
    items = order.get("items")

    if len(items) < 1:
        raise InvalidOrderOperation("An order must include items")

    for item in items:
        if item.get("quantity") < 1 or item.get("quantity") > 99:
            raise InvalidOrderOperation("Invalid item quantity")

    # Create the order header
    order = Order.objects.create(
        name=order.get("name"),
        address_1=order.get("address1"),
        address_2=order.get("address2"),
        town=order.get("town"),
        postcode=order.get("postcode"),
        phone=order.get("phone"),
        email=order.get("email"),
        delivery_instructions=order.get("delivery_instructions"),
    )

    # Loop through the items and save each of them, using the order id
    try:
        for item in items:
            Item.objects.get(pk=item.get("id"))

            OrderItem.objects.create(
                order_id=order.id,
                item_id=item.get("id"),
                quantity=item.get("quantity"),
            )
    except Item.DoesNotExist:
        raise InvalidItemError("Invalid item")

    return order
