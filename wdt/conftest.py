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
