from wdt.menu.resolvers.item import item_query
from wdt.menu.resolvers.menu import menu_query, menu_type
from wdt.menu.resolvers.section import section_query, section_type
from wdt.menu.resolvers.section_item import section_item_type

menu_schema = [
    item_query,
    menu_query,
    menu_type,
    section_query,
    section_type,
    section_item_type,
]
