from typing import List, Tuple

from django.conf import settings
from django.db.models import Model
from redis import Redis

r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Counter(object):
    @staticmethod
    def get_object_keys(object: Model) -> Tuple:
        return f"{object._meta.model_name}_counter", f"{object.id}"

    @classmethod
    def increase_counter(cls, object: Model) -> None:
        model_key, object_key = cls.get_object_keys(object)
        r.hincrby(model_key, object_key, 1)

    @classmethod
    def get_object_value(cls, object: Model) -> int:
        model_key, object_key = cls.get_object_keys(object)
        result = r.hget(model_key, object_key)
        if result:
            return int(result)
        return 0

    @staticmethod
    def get_most_displayed_objects(model_name: str, limit: int = 5) -> List:
        objects = r.hgetall(f"{model_name}_counter")
        return [
            int(k)
            for k, v in sorted(
                objects.items(), key=lambda item: int(item[1]), reverse=True
            )
        ][:limit]


class Recommender:
    def __init__(self):
        pass
