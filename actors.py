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

        return a * 0.5 * (a * b)

    def orientation(self, other):

        return (self.interests() * other.interests()) / \
               (self.magnitude() * other.magnitude())
