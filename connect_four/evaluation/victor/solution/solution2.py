class Solution:
    """A Solution is an application of a Rule that refutes at least one group.

    Two Solutions may or may not work together depending on which squares each
    consists of and which rule they are an application of.
    """
    def __init__(self, rule_instance):
        self.rule_instance = rule_instance
