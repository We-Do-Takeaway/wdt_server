import uuid
from http import HTTPStatus

import pytest


QUERY = """
query GetOrder($id:ID!) {
  order(id:$id) {
    id
    name
    address1
    address2
    town
    postcode
    phone
    email
    deliveryInstructions
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
class TestGetOrder:
    def test_get_valid_order(self, graphql_request, test_values):
        variables = {
            "id": test_values.ORDER_ID,
        }

        response = graphql_request(QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "order": {
                "id": test_values.ORDER_ID,
                "name": "Jim Smith",
                "address1": "10 The Lane",
                "address2": "Ealing",
                "town": "London",
                "postcode": "SW1 1A9",
                "phone": "555 123 4321",
                "email": "jsmith@acme.corp",
                "deliveryInstructions": "Under the mat",
                "items": [
                    {
                        "id": test_values.CHERRIES_ID,
                        "description": "Big bowl of cherries",
                        "name": "Bowl of cherries",
                        "photo": "bowlcherry.jpg",
                        "quantity": 1,
                    },
                ],
            },
        }

    def test_get_invalid_order(self, graphql_request, test_values):
        variables = {
            "id": str(uuid.uuid4()),
        }

        response = graphql_request(QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid order id"
