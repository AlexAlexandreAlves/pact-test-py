from pathlib import Path
from typing import Generator

import pytest
from pact import Pact, match

from src.api.cat_service import CatService, Cat


@pytest.fixture
def pact() -> Generator[Pact, None, None]:
    """Set up a Pact mock provider for cat consumer tests."""
    pact = Pact("cat-consumer", "cat-provider").with_specification("V4")
    yield pact
    pact.write_file(Path(__file__).parent / "../pacts")


def test_get_cat(pact: Pact) -> None:
    """Test the GET request for a cat by ID."""
    response: dict[str, object] = {
        "id": match.int(1),
        "name": match.str("Junin"),
        "age": match.int(3),
    }
    (
        pact.upon_receiving("A cat request")
        .given("the cat exists", id=1, name="Junin")
        .with_request("GET", "/cats/1")
        .will_respond_with(200)
        .with_body(response, content_type="application/json")
    )

    with pact.serve() as srv:
        client = CatService(str(srv.url))
        cat = client.get_cat(1)
        assert cat.name == "Junin"


def test_get_cats(pact: Pact) -> None:
    """Test the GET request for all cats."""
    response = [
        {
            "id": match.int(1),
            "name": match.str("Junin"),
            "age": match.int(3),
        },
        {
            "id": match.int(2),
            "name": match.str("Katara"),
            "age": match.int(5),
        }
    ]
    (
        pact.upon_receiving("A cats list request")
        .given("cats exist")
        .with_request("GET", "/cats")
        .will_respond_with(200)
        .with_body(response, content_type="application/json")
    )

    with pact.serve() as srv:
        client = CatService(str(srv.url))
        cats = client.get_cats()
        assert len(cats) == 2
        assert cats[0].name == "Junin"
        assert cats[1].name == "Katara"


def test_create_cat(pact: Pact) -> None:
    """Test the POST request to create a cat."""
    request_body = {
        "id": 11,
        "name": "Katara",
        "age": 5,
    }
    response_body = {
        "id": match.int(11),
        "name": match.str("Katara"),
        "age": match.int(5),
    }
    (
        pact.upon_receiving("A create cat request")
        .given("can create a cat")
        .with_request("POST", "/cats")
        .with_body(request_body, content_type="application/json")
        .will_respond_with(201)
        .with_body(response_body, content_type="application/json")
    )

    with pact.serve() as srv:
        client = CatService(str(srv.url))
        cat = client.create_cat(Cat(**request_body))
        assert cat.name == "Katara"
        assert cat.id == 11


def test_update_cat(pact: Pact) -> None:
    """Test the PUT request to update a cat."""
    request_body = {
        "name": "Aang",
        "age": 10,
    }
    response_body = {
        "name": match.str("Aang"),
        "age": match.int(10),
    }
    (
        pact.upon_receiving("An update cat request")
        .given("can update a cat", id=7)
        .with_request("PUT", "/cats/7")
        .with_body(request_body, content_type="application/json")
        .will_respond_with(201)
        .with_body(response_body, content_type="application/json")
    )

    with pact.serve() as srv:
        client = CatService(str(srv.url))
        updated_cat = client.update_cat(7, Cat(id=7, **request_body))
        assert updated_cat.name == "Aang"
        assert updated_cat.age == 10


def test_delete_cat(pact: Pact) -> None:
    """Test the DELETE request to delete a cat."""
    response_body = {
        "message": match.str("Cat Deleted Successfully")
    }
    (
        pact.upon_receiving("A delete cat request")
        .given("can delete a cat", id=3)
        .with_request("DELETE", "/cats/3")
        .will_respond_with(202)
        .with_body(response_body, content_type="application/json")
    )

    with pact.serve() as srv:
        client = CatService(str(srv.url))
        result = client.delete_cat(3)
        assert result["message"] == "Cat Deleted Successfully"
