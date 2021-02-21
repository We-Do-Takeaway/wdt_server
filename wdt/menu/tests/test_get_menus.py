from http import HTTPStatus

import pytest


QUERY = """
query GetMenus {
  menus {
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
    def test_get_menus(self, graphql_request, test_values):
        response = graphql_request(QUERY)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "menus": [
                {
                    "id": test_values.MENU_ID,
                    "name": "Cafe comfort and waffles",
                    "description": (
                        "The cafe is all about food to make you feel better when you can't face the world or "
                        + "feel like you are going crazy. Have an all day breakfast, your mothers Sunday roast "
                        + "or help yourself to the biggest bowl of ice-cream will lots of extras"
                    ),
                    "photo": "/images/default-thumbnail.png",
                },
            ],
        }
