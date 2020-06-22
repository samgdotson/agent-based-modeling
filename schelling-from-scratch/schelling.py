class SegregationModel(object):
    """
    This class runs a Schelling segregation
    model.
    """

    def __init__(self, dimensions, tolerance,
                 ratio_empty, num_races=2):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.tol = tolerance
        self.num_races = num_races
        self.ratio_empty = ratio_empty
        self.empty_houses = []
        self.agents = {}
