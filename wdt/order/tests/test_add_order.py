import copy
from http import HTTPStatus

import pytest
from dateutil.parser import isoparse

MUTATION_QUERY = """
mutation AddOrder($order: AddOrderInput!) {
  addOrder(order:$order) {
    id
    name
    address1
    address2
    town
    postcode
    phone
    email
    deliveryInstructions
    createdAt
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
NAME = "Fred Smith"
ADDRESS1 = "Address 1"
ADDRESS2 = "Address 2"
EMAIL = "fred@acme.corp"
TOWN = "Townsville"
POSTCODE = "PP1 1PP"
PHONE = "555 111 321"
INSTRUCTIONS = "Under the mat"

variables = {
    "order": {
        "name": NAME,
        "address1": ADDRESS1,
        "address2": ADDRESS2,
        "town": TOWN,
        "postcode": POSTCODE,
        "phone": PHONE,
        "email": EMAIL,
        "deliveryInstructions": INSTRUCTIONS,
        "items": [{"id": "124cec9c-0352-48a4-835f-5c4e3d45f69b", "quantity": 1}],
    },
}


@pytest.mark.django_db
@pytest.mark.usefixtures("example_data")
@pytest.mark.django_db(transaction=True)
class TestAddOrder:
    def test_add_fully_populated_valid_order(self, graphql_request, test_values):
        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        order = response.json()["data"]["addOrder"]

        assert order["name"] == NAME
        assert order["address1"] == ADDRESS1
        assert order["address2"] == ADDRESS2
        assert order["town"] == TOWN
        assert order["postcode"] == POSTCODE
        assert order["phone"] == PHONE
        assert order["email"] == EMAIL
        assert order["deliveryInstructions"] == INSTRUCTIONS
        assert order["items"] == [
            {
                "id": "124cec9c-0352-48a4-835f-5c4e3d45f69b",
                "description": "Big bowl of cherries",
                "name": "Bowl of cherries",
                "photo": "/images/default-thumbnail.png",
                "quantity": 1,
            },
        ]

    def test_add_minimally_populated_valid_order(self, graphql_request, test_values):
        minimal_variables = copy.deepcopy(variables)
        del minimal_variables["order"]["address2"]
        del minimal_variables["order"]["phone"]
        del minimal_variables["order"]["deliveryInstructions"]

        response = graphql_request(MUTATION_QUERY, variables=minimal_variables)
        assert response.status_code == HTTPStatus.OK
        order = response.json()["data"]["addOrder"]

        assert order["name"] == NAME
        assert order["address1"] == ADDRESS1
        assert order["address2"] is None
        assert order["town"] == TOWN
        assert order["postcode"] == POSTCODE
        assert order["phone"] is None
        assert order["email"] == EMAIL
        assert order["deliveryInstructions"] is None
        assert order["items"] == [
            {
                "id": "124cec9c-0352-48a4-835f-5c4e3d45f69b",
                "description": "Big bowl of cherries",
                "name": "Bowl of cherries",
                "photo": "/images/default-thumbnail.png",
                "quantity": 1,
            },
        ]

    def test_validate_created_at(self, graphql_request, test_values):
        response = graphql_request(MUTATION_QUERY, variables=variables)
        assert response.status_code == HTTPStatus.OK
        isoparse(response.json()["data"]["addOrder"]["createdAt"])

    def test_add_missing_address1(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        del test_variables["order"]["address1"]

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert len(errors) == 1

    def test_add_missing_items(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        del test_variables["order"]["items"]

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert len(errors) == 1

    def test_add_empty_items(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        test_variables["order"]["items"] = []

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert len(errors) == 1

    def test_add_missing_name(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        del test_variables["order"]["name"]

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert len(errors) == 1

    def test_add_missing_postcode(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        del test_variables["order"]["postcode"]

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert len(errors) == 1

    def test_add_missing_town(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        del test_variables["order"]["town"]

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert len(errors) == 1

    def test_add_invalid_item(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        test_variables["order"]["items"] = [
            {"id": "224cec9c-0352-48a4-835f-5c4e3d45f69b", "quantity": 1},
        ]

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert errors[0]["message"] == "Invalid item"

    def test_add_too_few_quantity(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        test_variables["order"]["items"][0]["quantity"] = 0

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK
        errors = response.json()["errors"]

        assert errors[0]["message"] == "Invalid item quantity"

    def test_add_too_high_quantity(self, graphql_request, test_values):
        test_variables = copy.deepcopy(variables)
        test_variables["order"]["items"][0]["quantity"] = 101

        response = graphql_request(MUTATION_QUERY, variables=test_variables)
        assert response.status_code == HTTPStatus.OK

        assert response.json()["errors"][0]["message"] == "Invalid item quantity"
