# Schelling Segregation Model in Python

This is a guide to programming the Schelling Segregation model from
Thomas Schelling's work in *Micromotives and Macrobehavior*. Along the way
we'll discuss topics related to coding like:
- Object Oriented Programming
- Agent-based modeling (and its limitations)
- Best practices (like descriptive docstrings)

I'll also include some of my thoughts on segregation in the United States.
To preview some of those thoughts, I think a segregation pattern that arose
from the Schelling model is an ideal to strive towards but is definitely not
how segregation operated (and continues to operate) in the United States.

#### Further Reading
1. *Micromotives and Macrobehavior* by Thomas C. Schelling
2. *The Color of Law* by Richard Rothstein

# Step 1: Define a class called ``SegregationModel``

Give this class the following parameters:
- Dimensions (height and width that determines our "city")
- A "tolerance" level
- The number of races
- A percentage of empty spaces (if the grid is filled 100% then the agents can't
move!)

We should also initialize a list of "agents" that live on the grid

```python
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

```
