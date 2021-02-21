import uuid
from http import HTTPStatus

import pytest


SHALLOW_QUERY = """
query GetSection($id:ID!) {
  section(id: $id) {
    id
    name
    description
    photo
    displayOrder
  }
}
"""

DEEP_QUERY = """
query GetSection($id:ID!) {
  section(id: $id) {
    id
    name
    description
    photo
    displayOrder
    items {
      id
      name
      description
      photo
      displayOrder
    }
  }
}
"""


@pytest.mark.django_db
@pytest.mark.usefixtures("example_data")
class TestGetSection:
    def test_get_valid_section(self, graphql_request, test_values):
        variables = {
            "id": test_values.DESERT_ID,
        }

        response = graphql_request(SHALLOW_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "section": {
                "id": test_values.DESERT_ID,
                "name": "Desert",
                "description": "The best stuff",
                "photo": "/images/default-thumbnail.png",
                "displayOrder": 2,
            },
        }

    def test_get_invalid_section(self, graphql_request, test_values):
        variables = {
            "id": str(uuid.uuid4()),
        }

        response = graphql_request(SHALLOW_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid section id"

    def test_get_valid_section_with_items(self, graphql_request, test_values):
        variables = {
            "id": test_values.DESERT_ID,
        }

        response = graphql_request(DEEP_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        items = response_data["section"]["items"]

        assert len(items) == 2

        assert items[0] == {
            "id": "83a40fc1-59dc-447d-afe0-6dcfe94bbf20",
            "name": "Chocolate ice-cream surprise",
            "description": "An amazing mixture of chocolate and cherries",
            "photo": "/images/default-thumbnail.png",
            "displayOrder": 1,
        }

        assert items[1] == {
            "id": "124cec9c-0352-48a4-835f-5c4e3d45f69b",
            "name": "Bowl of cherries",
            "description": "Big bowl of cherries",
            "photo": "/images/default-thumbnail.png",
            "displayOrder": 2,
        }
