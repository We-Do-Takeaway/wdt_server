from ariadne import ObjectType

from wdt.menu.models import Menu
from wdt.shared.exceptions import InvalidMenuError

menu_query = ObjectType("Query")
menu_type = ObjectType("Menu")


@menu_query.field("menu")
def resolve_menu(obj, info, *, id):
    try:
        return Menu.objects.get(pk=id)
    except Menu.DoesNotExist:
        raise InvalidMenuError("Invalid menu id")


@menu_query.field("menus")
def resolve_menus(_, info):
    return Menu.objects.order_by("name")


@menu_type.field("sections")
def resolve_menu_sections(menu, info):
    return menu.section_set.all().order_by("display_order")
