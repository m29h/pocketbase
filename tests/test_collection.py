from .connection import client, state, PocketBase

__all__ = ("client", "state")
from pocketbase.utils import ClientResponseError

from uuid import uuid4
import pytest


class TestCollectionService:
    def test_create(self, client: PocketBase, state):
        state.collection = client.collections.create(
            {
                "name": uuid4().hex,
                "type": "base",
                "schema": [
                    {
                        "name": "title",
                        "type": "text",
                        "required": True,
                        "options": {
                            "min": 10,
                        },
                    },
                ],
            }
        )

    def test_update(self, client: PocketBase, state):
        client.collections.update(
            state.collection.id,
            {
                "name": uuid4().hex,
                "schema": [
                    {
                        "name": "title",
                        "type": "text",
                        "required": True,
                        "options": {
                            "min": 10,
                        },
                    },
                    {
                        "name": "status",
                        "type": "bool",
                    },
                ],
            },
        )

    def test_delete(self, client: PocketBase, state):
        client.collections.delete(state.collection.id)
        with pytest.raises(ClientResponseError) as exc:
            client.collections.delete(state.collection.id, uuid4().hex)
        assert exc.value.status == 404  # double already deleted


def test_delete_nonexisting_exception(client):
    with pytest.raises(ClientResponseError) as exc:
        client.collections.delete(uuid4().hex, uuid4().hex)
    assert exc.value.status == 404  # delete nonexisting


def test_get_nonexisting_exception(client):
    with pytest.raises(ClientResponseError) as exc:
        client.collections.get_one(uuid4().hex)
    assert exc.value.status == 404
