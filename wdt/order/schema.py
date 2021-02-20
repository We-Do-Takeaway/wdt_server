from wdt.order.resolvers.order import order_query, order_type
from wdt.order.resolvers.order_item import order_item_type
from wdt.order.resolvers.order_mutations import order_mutation

order_schema = [
    order_query,
    order_mutation,
    order_type,
    order_item_type,
]
