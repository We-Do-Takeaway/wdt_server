from http import HTTPStatus

import pytest


QUERY = """
query GetSections {
  sections {
    id
    name
    description
    photo
    displayOrder
  }
}
"""


@pytest.mark.django_db
@pytest.mark.usefixtures("example_data")
class TestGetSections:
    def test_get_sections(self, graphql_request, test_values):
        response = graphql_request(QUERY)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "sections": [
                {
                    "id": "6736bb37-64dc-4f3e-9251-4c2d47eef640",
                    "name": "Desert",
                    "description": "The best stuff",
                    "photo": "desert.jpg",
                    "displayOrder": 2,
                },
                {
                    "id": "ac2f8c68-f358-4708-9e81-fba155fab20f",
                    "name": "Main",
                    "description": "Stuff to fill you up",
                    "photo": "main.jpg",
                    "displayOrder": 1,
                },
            ],
        }
