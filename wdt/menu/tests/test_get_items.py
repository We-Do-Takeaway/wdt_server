from http import HTTPStatus

import pytest


QUERY = """
query GetItems {
  items {
    id
    name
    description
    photo
  }
}
"""


@pytest.mark.django_db
@pytest.mark.usefixtures("example_data")
class TestGetMenus:
    def test_get_items(self, graphql_request):
        response = graphql_request(QUERY)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "items": [
                {
                    "id": "124cec9c-0352-48a4-835f-5c4e3d45f69b",
                    "name": "Bowl of cherries",
                    "description": "Big bowl of cherries",
                    "photo": "/images/default-thumbnail.png",
                },
                {
                    "id": "83a40fc1-59dc-447d-afe0-6dcfe94bbf20",
                    "name": "Chocolate ice-cream surprise",
                    "description": "An amazing mixture of chocolate and cherries",
                    "photo": "/images/default-thumbnail.png",
                },
                {
                    "id": "a4b463c9-f786-4945-af19-fb3103d3984b",
                    "name": "Plate of sausages",
                    "description": "Big bowl of sausages",
                    "photo": "/images/default-thumbnail.png",
                },
            ],
        }
