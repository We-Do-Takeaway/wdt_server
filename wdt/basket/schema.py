from wdt.basket.resolvers.basket import basket_query, basket_type
from wdt.basket.resolvers.basket_item import basket_item_type

basket_schema = [
    basket_query,
    basket_type,
    basket_item_type,
]
