from ariadne import ObjectType

from wdt.menu.models import Item
from wdt.shared.exceptions import InvalidItemError

item_query = ObjectType("Query")


@item_query.field("item")
def resolve_item(obj, info, *, id):
    try:
        return Item.objects.get(pk=id)
    except Item.DoesNotExist:
        raise InvalidItemError("Invalid item id")


@item_query.field("items")
def resolve_menus(_, info):
    return Item.objects.order_by("name")
