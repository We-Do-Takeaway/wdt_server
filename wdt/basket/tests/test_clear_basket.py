from http import HTTPStatus

import pytest


MUTATION_QUERY = """
mutation ClearBasket($basketId: ID!) {
  clearBasket(basketId: $basketId) {
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
class TestClearBasket:
    def test_clear_valid_basket(self, graphql_request, test_values):
        variables = {"basketId": test_values.EXISTING_BASKET_ID}

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        response_data = response.json()["data"]
        assert response_data == {
            "clearBasket": {
                "id": test_values.EXISTING_BASKET_ID,
                "items": [],
            },
        }

    def test_clear_invalid_basket(self, graphql_request, test_values):
        variables = {"basketId": test_values.INVALID_BASKET_ID}

        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]
        assert errors[0]["message"] == "Invalid basket id"
