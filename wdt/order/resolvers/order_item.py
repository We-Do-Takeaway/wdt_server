from ariadne import ObjectType

order_item_type = ObjectType("OrderItem")


@order_item_type.field("id")
def resolve_id(basketitem, info):
    return basketitem.item_id


@order_item_type.field("name")
def resolve_name(basketitem, info):
    return basketitem.item.name


@order_item_type.field("description")
def resolve_description(basketitem, info):
    return basketitem.item.description


@order_item_type.field("photo")
def resolve_photo(basketitem, info):
    return basketitem.item.photo


@order_item_type.field("quantity")
def resolve_quantity(basketitem, info):
    return basketitem.quantity
