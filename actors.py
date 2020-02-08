import numpy as np
import random as r

from utils.Identifers import Identifier


class Actor:
    def __init__(self, interests):
        self._id = Identifier.get_id("Actor")
        self._interests = np.array(interests)
        self._social_norm = np.array(interests)
        self._social_integrity = 0.0
        self._social_desirability = False

    def magnitude(self):
        return np.linalg.norm(self._interests)

    def interests(self):
        if not self._social_desirability:
            result = self._interests
        else:
            result = np.array([x if r.random() <= self._social_integrity else y
                               for x, y in zip(self._interests, self._social_norm)])

        return result

    def orientation_of_action(self, other):
        a = self.interests()
        b = other.interests()
        result = np.dot(a, 0.5 * (a + b))
        return result

    def orientation(self, other):
        a = self.interests()
        b = other.interests()
        _a = self.magnitude()
        _b = other.magnitude()

        return np.dot(a, b) / (_a * _b)

    def obeys_social_pressure(self):
        return self._social_desirability

    def set_social_desirability(self, p, d, norm):
        self._social_norm = np.array(norm)
        self._social_integrity = (p - d) + r.random()*2*d
        self._social_integrity = 1.0 if self._social_integrity >= 1.0 else self._social_desirability
        self._social_desirability = True

    def __str__(self):
        return "Actor : {}".format(self.interests())
