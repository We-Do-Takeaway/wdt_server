from ariadne import ObjectType

from wdt.menu.models import Menu, Section

query = ObjectType("Query")
menu_type = ObjectType("Menu")


@query.field("menu")
def resolve_menu(obj, info, *, id):
    try:
        return Menu.objects.get(pd=id)
    except Menu.DoesNotExist:
        return None


@query.field("menus")
def resolve_menus(_, info):
    return Menu.objects.order_by("name")


@menu_type.field("sections")
def resolve_menu_sections(menu, info):
    return menu.section_set.all().order_by('display_order')
