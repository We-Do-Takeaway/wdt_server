import uuid
from http import HTTPStatus

import pytest


QUERY = """
query GetBasket($id:ID!) {
  basket(id:$id) {
    id
    items {
      id
      description
      name
      photo
      quantity
    }
  }
}
"""


@pytest.mark.django_db
@pytest.mark.usefixtures("example_data")
class TestGetBasket:
    def test_get_valid_basket(self, graphql_request, test_values):
        variables = {
            "id": test_values.BASKET_ID,
        }

        response = graphql_request(QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "basket": {
                "id": test_values.BASKET_ID,
                "items": [
                    {
                        "id": test_values.CHERRIES_ID,
                        "description": "Big bowl of cherries",
                        "name": "Bowl of cherries",
                        "photo": "/images/default-thumbnail.png",
                        "quantity": 1,
                    },
                ],
            },
        }

    def test_get_invalid_menu(self, graphql_request, test_values):
        fake_id = str(uuid.uuid4())
        variables = {
            "id": fake_id,
        }

        response = graphql_request(QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "basket": {
                "id": fake_id,
                "items": [],
            },
        }
