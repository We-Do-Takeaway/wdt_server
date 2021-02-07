from http import HTTPStatus

import pytest


MUTATION_QUERY = """
mutation AddBasketItem(
    $basketId: ID!,
    $basketItem: BasketItemInput!
) {
  addBasketItem(
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
class TestAddBasketItem:
    def test_add_valid_item_to_existing_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": test_values.SAUSAGES_ID,
                "quantity": 1,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "addBasketItem": {
                "id": test_values.EXISTING_BASKET_ID,
                "items": [
                    {
                        "id": test_values.CHERRIES_ID,
                        "name": test_values.CHERRIES_NAME,
                        "quantity": 1,
                    },
                    {
                        "id": test_values.SAUSAGES_ID,
                        "name": test_values.SAUSAGES_NAME,
                        "quantity": 1,
                    },
                ],
            },
        }

    def test_add_valid_item_to_unknown_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.NEW_BASKET_ID,
            "basketItem": {
                "itemId": test_values.SAUSAGES_ID,
                "quantity": 1,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "addBasketItem": {
                "id": test_values.NEW_BASKET_ID,
                "items": [
                    {
                        "id": test_values.SAUSAGES_ID,
                        "name": test_values.SAUSAGES_NAME,
                        "quantity": 1,
                    },
                ],
            },
        }

    def test_add_invalid_item_to_existing_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": test_values.INVALID_ITEM_ID,
                "quantity": 1,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        errors = response.json()["errors"]

        assert errors[0]["message"] == "Invalid item id"

    def test_add_duplicate_item_to_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": test_values.CHERRIES_ID,
                "quantity": 1,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "addBasketItem": {
                "id": test_values.EXISTING_BASKET_ID,
                "items": [
                    {
                        "id": test_values.CHERRIES_ID,
                        "name": test_values.CHERRIES_NAME,
                        "quantity": 2,
                    },
                ],
            },
        }

    def test_too_many_to_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.NEW_BASKET_ID,
            "basketItem": {
                "itemId": test_values.SAUSAGES_ID,
                "quantity": 99,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert errors[0]["message"] == "Invalid quantity"

    def test_too_few_to_basket(self, graphql_request, test_values):
        variables = {
            "basketId": test_values.NEW_BASKET_ID,
            "basketItem": {
                "itemId": test_values.SAUSAGES_ID,
                "quantity": -1,
            },
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert errors[0]["message"] == "Invalid quantity"
