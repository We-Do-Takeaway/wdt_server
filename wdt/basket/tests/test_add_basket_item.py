from http import HTTPStatus

import pytest

from wdt.basket.models import BasketItem

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

EXISTING_BASKET_ID = "b63920b5-d2ca-4e5a-a7c5-05b7cbf00cc3"
NEW_BASKET_ID = "b63920b5-d2ca-4e5a-a7c5-05b7cbf00cc4"
SAUSAGES_ID = "a4b463c9-f786-4945-af19-fb3103d3984b"
CHERRIES_ID = "124cec9c-0352-48a4-835f-5c4e3d45f69b"
INVALID_ITEM_ID = "124cec9c-0352-48a4-835f-5c4e3d45f69c"


@pytest.mark.django_db
@pytest.mark.usefixtures("example_data")
class TestAddBasketItem:
    def test_add_valid_item_to_existing_basket(self, graphql_request):
        variables = {
            "basketId": EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": SAUSAGES_ID,
                "quantity": 1
            }
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "addBasketItem": {
                "id": EXISTING_BASKET_ID,
                "items": [
                    {
                        "id": SAUSAGES_ID,
                        "name": "Plate of sausages",
                        "quantity": 1,
                    }
                ]
            }
        }

    def test_add_valid_item_to_unknown_basket(self, graphql_request):
        variables = {
            "basketId": NEW_BASKET_ID,
            "basketItem": {
                "itemId": SAUSAGES_ID,
                "quantity": 1
            }
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "addBasketItem": {
                "id": NEW_BASKET_ID,
                "items": [
                    {
                        "id": SAUSAGES_ID,
                        "name": "Plate of sausages",
                        "quantity": 1,
                    }
                ]
            }
        }

    def test_add_invalid_item_to_existing_basket(self, graphql_request):
        variables = {
            "basketId": EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": INVALID_ITEM_ID,
                "quantity": 1
            }
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        errors = response.json()["errors"]

        assert errors[0]["message"] == "The item id does not exist"

    def test_add_second_item_to_basket(self, graphql_request):
        basket_item = BasketItem(
            basket_id=EXISTING_BASKET_ID,
            item_id=SAUSAGES_ID,
            quantity=1,
        )

        basket_item.save()

        variables = {
            "basketId": EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": CHERRIES_ID,
                "quantity": 1
            }
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "addBasketItem": {
                "id": EXISTING_BASKET_ID,
                "items": [
                    {
                        "id": CHERRIES_ID,
                        "name": "Bowl of cherries",
                        "quantity": 1,
                    },
                    {
                        "id": SAUSAGES_ID,
                        "name": "Plate of sausages",
                        "quantity": 1,
                    },
                ]
            }
        }

    def test_add_duplicate_item_to_basket(self, graphql_request):
        basket_item = BasketItem(
            basket_id=EXISTING_BASKET_ID,
            item_id=SAUSAGES_ID,
            quantity=1,
        )

        basket_item.save()

        variables = {
            "basketId": EXISTING_BASKET_ID,
            "basketItem": {
                "itemId": SAUSAGES_ID,
                "quantity": 1
            }
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "addBasketItem": {
                "id": EXISTING_BASKET_ID,
                "items": [
                    {
                        "id": SAUSAGES_ID,
                        "name": "Plate of sausages",
                        "quantity": 2,
                    }
                ]
            }
        }

    def test_too_many_to_basket(self, graphql_request):
        variables = {
            "basketId": NEW_BASKET_ID,
            "basketItem": {
                "itemId": SAUSAGES_ID,
                "quantity": 99
            }
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert errors[0]["message"] == "Too many items added"
