import uuid
from http import HTTPStatus

import pytest


MUTATION_QUERY = """
mutation RemoveBasketItem(
    $basketId: ID!,
    $itemId: ID!
) {
  removeBasketItem(
    basketId: $basketId,
    itemId: $itemId
  ) {
    id
    items {
      id
      name
      quantity
    }
  }
}
"""


@pytest.mark.django_db
@pytest.mark.usefixtures("example_data")
class TestRemoveBasketItem:
    def test_remove_item_in_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.BASKET_ID,
            "itemId": test_values.CHERRIES_ID,
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "removeBasketItem": {
                "id": test_values.BASKET_ID,
                "items": [],
            },
        }

    def test_remove_invalid_item_in_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.BASKET_ID,
            "itemId": test_values.SAUSAGES_ID,
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid item id"

    def test_remove_item_in_invalid_basket(self, graphql_request, test_values):
        variables = {
            "basketId": str(uuid.uuid4()),
            "itemId": test_values.CHERRIES_ID,
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid basket id"
