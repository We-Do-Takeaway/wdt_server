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
    def test_add_valid_item_to_existing_basket(self, graphql_request):
        variables = {
            "basketId": "b63920b5-d2ca-4e5a-a7c5-05b7cbf00cc3",
            "basketItem": {
                "itemId": "a4b463c9-f786-4945-af19-fb3103d3984b",
                "quantity": 1
            }
        }

        response = graphql_request(MUTATION_QUERY, variables=variables)

        response_data = response.json()["data"]

        assert response.status_code == HTTPStatus.OK

        assert response_data == {
            "addBasketItem": {
                "id": "b63920b5-d2ca-4e5a-a7c5-05b7cbf00cc3",
                "items": [
                    {
                        "id": "a4b463c9-f786-4945-af19-fb3103d3984b",
                        "name": "Plate of sausages",
                        "quantity": 1,
                    }
                ]
            }
        }


