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
    NEW_BASKET_ID = "b63920b5-d2ca-4e5a-a7c5-05b7cbf00cc5"
    EXISTING_BASKET_ID = "03b9d6a5-2561-4567-90e9-452e8b39ce86"
    INVALID_BASKET_ID = "b63920b5-d2ca-4e5a-a7c5-05b7cbf00cc4"
    SAUSAGES_ID = "a4b463c9-f786-4945-af19-fb3103d3984b"
    SAUSAGES_NAME = "Plate of sausages"
    CHERRIES_ID = "124cec9c-0352-48a4-835f-5c4e3d45f69b"
    CHERRIES_NAME = "Bowl of cherries"
    INVALID_ITEM_ID = "124cec9c-0352-48a4-835f-5c4e3d45f69c"


@pytest.fixture
def test_values():
    return CommonTestData
