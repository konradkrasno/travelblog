from .recommender import Counter


class DisplayCounterMixin(object):
    def get_context_data(self, **kwargs):
        data = super().get_context_data()
        if self.request.user != self.object.author:
            Counter.increase_counter(self.object)
        data["number_of_displays"] = Counter.get_object_value(self.object)
        return data
