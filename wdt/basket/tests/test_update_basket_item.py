from http import HTTPStatus

import pytest

MUTATION_QUERY = """
mutation UpdateBasketItem(
    $basketId: ID!,
    $basketItem: BasketItemInput!
) {
  updateBasketItem(
    basketId: $basketId,
    basketItem: $basketItem
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
class TestUpdateBasketItem:
    def test_update_valid_item_in_existing_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": test_values.CHERRIES_ID,
                "quantity": 10,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "updateBasketItem": {
                "id": test_values.EXISTING_BASKET_ID,
                "items": [
                    {
                        "id": test_values.CHERRIES_ID,
                        "name": test_values.CHERRIES_NAME,
                        "quantity": 10,
                    },
                ],
            },
        }

    def test_update_valid_item_to_unknown_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.INVALID_BASKET_ID,
            "basketItem": {
                "itemId": test_values.CHERRIES_ID,
                "quantity": 1,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid basket id"

    def test_update_item_not_in_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": test_values.SAUSAGES_ID,
                "quantity": 1,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid item id"

    def test_update_to_too_many_items(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": test_values.CHERRIES_ID,
                "quantity": 101,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert errors[0]["message"] == "Invalid quantity"

    def test_update_to_too_few_items(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": test_values.CHERRIES_ID,
                "quantity": -1,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert errors[0]["message"] == "Invalid quantity"

    def test_update_item_quantity_to_zero_removes_item(
        self,
        graphql_request,
        test_values,
    ):
        variables = {
            "basketId": test_values.EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": test_values.CHERRIES_ID,
                "quantity": 0,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "updateBasketItem": {
                "id": test_values.EXISTING_BASKET_ID,
                "items": [],
            },
        }
