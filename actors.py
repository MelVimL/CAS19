import numpy as np

from utils.Identifers import Identifier


class Actor:
    def __init__(self, interests):
        self._id = Identifier.get_id("Actor")
        self._interests = np.array(interests)

    def magnitude(self):
        return np.linalg.norm(self._interests)

    def interests(self):
        return self._interests

    def orientation_of_action(self, other):
        a = self.interests()
        b = other.interests()
        result = np.dot(a, 0.5 * (a+b))
        return result

    def orientation(self, other):
        a = self.interests()
        b = other.interests()
        _a = self.magnitude()
        _b = other.magnitude()

        return np.dot(a, b) / (_a * _b)

    def __str__(self):
        return "Actor : {}".format(self.interests())
