import pytest
from django.core.management import call_command
from django.test import Client


@pytest.fixture
def graphql_request():
    return _execute_graphql_query


@pytest.fixture
def example_data(db):
    print("Loading fixtures")
    call_command("loaddata", "data.json", verbosity=3)
    print("Fixtures loaded")


def _execute_graphql_query(query, variables=None, **kwargs):
    client = Client()

    data = {
        "query": query,
        **({"variables": variables} if variables is not None else {}),
    }

    return client.post(
        "/graphql/",
        content_type="application/json",
        data=data,
        **kwargs,
    )


class CommonTestData:
    BASKET_ID = "03b9d6a5-2561-4567-90e9-452e8b39ce86"
    CHERRIES_ID = "124cec9c-0352-48a4-835f-5c4e3d45f69b"
    DESERT_ID = "6736bb37-64dc-4f3e-9251-4c2d47eef640"
    MENU_ID = "11ca8caa-e5dc-494d-bcfd-79fdeb34b1b1"
    ORDER_ID = "305329a8-4111-41e0-9d5e-c81a00e7bc97"
    SAUSAGES_ID = "a4b463c9-f786-4945-af19-fb3103d3984b"


@pytest.fixture
def test_values():
    return CommonTestData
