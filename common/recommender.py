from typing import List, Tuple

from django.conf import settings
from django.db.models import Model
from redis import Redis

r = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class Counter(object):
    def __init__(self, suffix: str):
        self._suffix = suffix

    def get_object_keys(self, obj: Model) -> Tuple:
        return f"{obj._meta.model_name}{self._suffix}", f"{obj.id}"

    def increase_counter(self, obj: Model) -> None:
        model_key, object_key = self.get_object_keys(obj)
        r.zincrby(model_key, 1, object_key)

    def get_object_value(self, obj: Model) -> int:
        model_key, object_key = self.get_object_keys(obj)
        result = r.zscore(model_key, object_key)
        if result:
            return int(result)
        return 0

    def get_most_displayed_objects(self, model_name: str, limit: int = 5) -> List:
        model_key = f"{model_name}{self._suffix}"
        if limit < 1:
            return []
        objects = r.zrange(model_key, 0, limit-1, desc=True)
        return [int(_id) for _id in objects]


class Recommender:
    def __init__(current_user_name: str):
        self._current_user_name = current_user_name

    @property
    def current_user_key(self) -> str:
        return self.get_user_key(self._current_user_name)

    @property
    def current_user_name(self) -> str:
        return set._current_user_name

    @staticmethod
    def get_user_key(username: str) -> str:
        return f"usr:{username}:seen_objects"

    @staticmethod
    def get_object_key(obj: Model) -> str:
        return f"object:{obj._meta.model_name}:{obj.id}:viewers"

    @staticmethod
    def get_object_name(obj: Model) -> str:
        return f"object:{obj._meta.model_name}:{obj.id}"
    
    def relate_current_user_with_object(self, obj: Model) -> None:
        r.sadd(self.current_user_key, self.get_object_name(obj))
        r.sadd(self.get_object_key(obj), self.current_user_name)

    # @staticmethod
    # def get_object_model_and_id(obj_name: str, suffix: str) -> Tuple:
    #     model_name, _id = obj_name.split(":")[1:]
    #     return f"{model_name}{suffix}", _id

    @classmethod
    def retrieve_objects_by_displays(cls, model_name: str, objects: List, limit: int) -> List:
        # displays_counter = Counter(":display_count")
        flat_ids = "".join([obj_name.split(":")[-1] for obj_name in objects])
        tmp_key = f"{model_name}{flat_ids}"
        r.zunionstore(tmp_key, )


    @classmethod
    def get_recommendations(cls, model_name: str, username: str, limit: int) -> List:
        objects = r.smembers(self.get_user_key(username))
        object_keys = [f"{obj_name}:viewers" for obj_name in objects if model_name in object_name]
        users = r.sunion(object_keys)
        objects = [r.sdiff(self.get_user_key(user), self.get_user_key(username)) for user in users if user != username]
        return self.retrieve_objects_by_displays(model_name, objects, limit)
