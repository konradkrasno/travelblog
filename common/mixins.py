from .recommender import Counter


class DisplayCounterMixin(object):
    def get_context_data(self, **kwargs):
        display_counter = Counter(":display_count")
        data = super().get_context_data()
        if self.request.user != self.object.author:
            display_counter.increase_counter(self.object)
        data["number_of_displays"] = display_counter.get_object_value(self.object)
        return data


class RecommenderMixin(object):
    pass
