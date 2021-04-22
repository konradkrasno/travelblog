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

    def get_most_popular_objects(self, model_name: str, limit: int = 5) -> List:
        model_key = f"{model_name}{self._suffix}"
        if limit < 1:
            return []
        objects = r.zrange(model_key, 0, limit - 1, desc=True)
        return [int(_id) for _id in objects]


class Recommender:
    def __init__(self, current_user_name: str):
        self._current_user_name = current_user_name

    @property
    def current_user_key(self) -> str:
        return self.get_user_key(self._current_user_name)

    @property
    def current_user_name(self) -> str:
        return self._current_user_name

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

    @classmethod
    def get_recommendations(cls, model_name: str, username: str, limit: int) -> List:
        usr_obj = r.smembers(cls.get_user_key(username))
        usr_obj_keys = [
            f"{obj_name.decode()}:viewers"
            for obj_name in usr_obj
            if model_name in obj_name.decode()
        ]
        if usr_obj_keys:
            users = r.sunion(usr_obj_keys)
            other_usr_obj = [
                r.sdiff(cls.get_user_key(user.decode()), cls.get_user_key(username))
                for user in users
                if user.decode() != username
            ]
            tmp_key = f"tmp_key:{username}:{model_name}"
            for objects in other_usr_obj:
                for obj in objects:
                    r.zincrby(tmp_key, 1, obj)
            if limit < 1:
                return []
            result = r.zrange(tmp_key, 0, limit - 1, desc=True)
            r.delete(tmp_key)
            return [int(obj.decode().split(":")[-1]) for obj in result]
        return []
