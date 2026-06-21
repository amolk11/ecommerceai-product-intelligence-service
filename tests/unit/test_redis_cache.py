import json
from unittest.mock import MagicMock

import redis

from app.cache.redis_cache import RedisCache


def test_get_returns_deserialized_value():
    client = MagicMock()
    client.get.return_value = json.dumps(
        {
            "product_id": 101,
            "score": 97.2,
        }
    )

    cache = RedisCache(client)

    result = cache.get("test-key")

    assert result == {
        "product_id": 101,
        "score": 97.2,
    }


def test_get_returns_none_when_key_missing():
    client = MagicMock()
    client.get.return_value = None

    cache = RedisCache(client)

    result = cache.get("missing-key")

    assert result is None


def test_get_returns_none_when_redis_fails():
    client = MagicMock()
    client.get.side_effect = redis.RedisError("redis down")

    cache = RedisCache(client)

    result = cache.get("test-key")

    assert result is None


def test_get_returns_none_when_json_invalid():
    client = MagicMock()
    client.get.return_value = "not-json"

    cache = RedisCache(client)

    result = cache.get("test-key")

    assert result is None


def test_set_stores_serialized_value():
    client = MagicMock()

    cache = RedisCache(client)

    payload = {
        "product_id": 101,
        "score": 97.2,
    }

    cache.set(
        key="test-key",
        value=payload,
        ttl=300,
    )

    client.set.assert_called_once_with(
        name="test-key",
        value=json.dumps(payload),
        ex=300,
    )


def test_set_handles_redis_error():
    client = MagicMock()
    client.set.side_effect = redis.RedisError("redis down")

    cache = RedisCache(client)

    cache.set(
        key="test-key",
        value={"a": 1},
        ttl=300,
    )

    client.set.assert_called_once()


def test_ping_returns_true():
    client = MagicMock()
    client.ping.return_value = True

    cache = RedisCache(client)

    assert cache.ping() is True


def test_ping_returns_false_on_error():
    client = MagicMock()
    client.ping.side_effect = redis.RedisError("redis down")

    cache = RedisCache(client)

    assert cache.ping() is False


def test_delete_calls_redis_delete():
    client = MagicMock()

    cache = RedisCache(client)

    cache.delete("test-key")

    client.delete.assert_called_once_with("test-key")


def test_delete_handles_redis_error():
    client = MagicMock()
    client.delete.side_effect = redis.RedisError("redis down")

    cache = RedisCache(client)

    cache.delete("test-key")

    client.delete.assert_called_once_with("test-key")
