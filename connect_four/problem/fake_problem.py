from connect_four.problem.problem import Problem


class FakeProblem(Problem):
    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, FakeProblem):
            return self.name == other.name
        return False

    def __hash__(self):
        return self.name.__hash__()
