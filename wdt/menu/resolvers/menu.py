from ariadne import ObjectType

from wdt.menu.models import Menu

query = ObjectType("Query")


@query.field("menu")
def resolve_menu(obj, info, *, id):
    try:
        return Menu.objects.get(pd=id)
    except Menu.DoesNotExist:
        return None


@query.field("menus")
def resolve_menus(_, info):
    return Menu.objects.order_by("name")

