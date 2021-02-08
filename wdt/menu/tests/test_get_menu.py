import uuid
from http import HTTPStatus

import pytest


SHALLOW_QUERY = """
query GetMenu($id:ID!) {
  menu(id: $id) {
    id
    name
    description
    photo
  }
}
"""

DEEP_QUERY = """
query GetMenu($id:ID!) {
  menu(id: $id) {
    id
    name
    description
    photo
    sections {
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
class TestGetMenu:
    def test_get_valid_menu(self, graphql_request, test_values):
        variables = {
            "id": test_values.MENU_ID,
        }

        response = graphql_request(SHALLOW_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "menu": {
                "id": test_values.MENU_ID,
                "name": "Cafe comfort and waffles",
                "description": (
                    "The cafe is all about food to make you feel better when you can't face the world or "
                    + "feel like you are going crazy. Have an all day breakfast, your mothers Sunday roast "
                    + "or help yourself to the biggest bowl of ice-cream will lots of extras"
                ),
                "photo": "cafe.jpg",
            },
        }

    def test_get_invalid_menu(self, graphql_request, test_values):
        variables = {
            "id": str(uuid.uuid4()),
        }

        response = graphql_request(SHALLOW_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid menu id"

    def test_get_valid_menu_with_sections(self, graphql_request, test_values):
        variables = {
            "id": test_values.MENU_ID,
        }

        response = graphql_request(DEEP_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        sections = response_data["menu"]["sections"]

        assert sections == [
            {
                "id": "ac2f8c68-f358-4708-9e81-fba155fab20f",
                "name": "Main",
                "description": "Stuff to fill you up",
                "photo": "main.jpg",
                "displayOrder": 1,
            },
            {
                "id": "6736bb37-64dc-4f3e-9251-4c2d47eef640",
                "name": "Desert",
                "description": "The best stuff",
                "photo": "desert.jpg",
                "displayOrder": 2,
            },
        ]
