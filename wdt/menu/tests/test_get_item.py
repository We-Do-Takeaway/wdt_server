import uuid
from http import HTTPStatus

import pytest


QUERY = """
query GetItem($id:ID!) {
  item(id: $id) {
    id
    name
    description
    photo
  }
}
"""


@pytest.mark.django_db
@pytest.mark.usefixtures("example_data")
class TestGetItem:
    def test_get_valid_item(self, graphql_request, test_values):
        variables = {
            "id": test_values.SAUSAGES_ID,
        }

        response = graphql_request(QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "item": {
                "id": test_values.SAUSAGES_ID,
                "name": "Plate of sausages",
                "description": "Big bowl of sausages",
                "photo": "plate-sausages.jpg",
            },
        }

    def test_get_invalid_item(self, graphql_request, test_values):
        variables = {
            "id": str(uuid.uuid4()),
        }

        response = graphql_request(QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid item id"
