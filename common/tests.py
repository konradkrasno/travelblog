from unittest.mock import patch

from django.test import TestCase

from .recommender import Counter


class TestCounter(TestCase):
    @patch("redis.Redis.hgetall")
    def test_get_most_displayed_objects(self, mock_hgetall):
        mock_hgetall.return_value = {b"1": b"7", b"3": b"1", b"6": b"1", b"4": b"5"}
        assert Counter.get_most_displayed_objects("fake", limit=3) == [1, 4, 3]
