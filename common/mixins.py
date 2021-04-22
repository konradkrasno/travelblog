from .recommender import Counter, Recommender


class DisplayCounterMixin(object):
    def get_context_data(self, **kwargs):
        display_counter = Counter(":display_count")
        recommender = Recommender(self.request.user.username)
        data = super().get_context_data()
        if self.request.user != self.object.author:
            display_counter.increase_counter(self.object)
            recommender.relate_current_user_with_object(self.object)
        data["number_of_displays"] = display_counter.get_object_value(self.object)
        return data
