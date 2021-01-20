class SimplePlan:
    def __init__(self, responses=None, availabilities=None):
        if responses is None:
            responses = dict()
        if availabilities is None:
            availabilities = set()
        self.responses = responses
        self.availabilities = availabilities

    def __eq__(self, other):
        if isinstance(other, SimplePlan):
            return self.responses == other.responses and self.availabilities == other.availabilities
        return False

    def merge(self, simple_plan):
        pass

    def add_responses(self, responses):
        pass

    def add_availability(self, availability):
        pass


class SimplePlanBuilder:
    def __init__(self, plans=None):
        if plans is None:
            plans = []
        self.plans = plans.copy()

    def add(self, plan):
        pass

    def build(self):
        pass
