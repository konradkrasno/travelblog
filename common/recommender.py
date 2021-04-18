from redis import Redis
from django.conf import settings
from django.db.models import Model

r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Counter(object):
    @staticmethod
    def get_object_key(object: Model) -> str:
        return f"{object._meta.model_name}:{object.id}"

    @classmethod
    def increase_counter(cls, object: Model) -> None:
        object_key = cls.get_object_key(object)
        r.incrby(object_key, 1)

    @classmethod
    def get_object_value(cls, object: Model) -> int:
        object_key = cls.get_object_key(object)
        return int(r.get(object_key))


class Recommender:
    def __init__(self):
        pass
