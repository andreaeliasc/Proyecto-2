from lib import *
from math import sqrt
from sphere import *

#https://github.com/tobycyanide/pytracer/blob/master/raytracer/shapes.py
class Cylinder(object):

    def __init__(self, radius, height, center, material):
        self.radius = radius
        self.height = height
        self.closed = False
        self.center = center
        self.material = material

    def ray_intersect(self, origin, direction):
        a = direction[0] ** 2 + direction[2] ** 2
        if abs(a) < 0.0001: #epsilon = 0.0001
            return None

        b = 2 * (
            direction[0] * (origin[0] - self.center[0])
            + direction[2] * (origin[2] - self.center[2])
        )
        c = (
            (origin[0] - self.center[0]) ** 2
            + (origin[2] - self.center[2]) ** 2
            - (self.radius ** 2)
        )

        discriminant = b ** 2 - 4 * (a * c)

        if discriminant < 0.0:
            return None

        t0 = (-b - sqrt(discriminant)) / (2 * a)
        t1 = (-b + sqrt(discriminant)) / (2 * a)

        if t0 > t1:
            t0, t1, t1, t0

        y0 = origin[1] + t0 * direction[1]
        if self.center[1] < y0 and y0 <= (self.center[1] + self.height):
            hit = sum(origin, mul(direction,t0))
            normal = norm(sub(self.center, hit))
            return Intersect(distance = t0,
                             point = hit,
                             normal = normal
                             )

        y1 = origin[1] + t1 * direction[1]
        if self.center[1] < y1 and y1 <= (self.center[1] + self.height):
            hit = sum(origin, mul(direction, t1))
            normal = norm(sub(self.center, hit))
            return Intersect(distance=t1,
                             point = hit,
                             normal = normal
            )
        return self.intersect_caps(origin, direction)

    def check_cap(self, origin, direction, t):
        x = origin[0] + t * direction[0]
        z = origin[2] + t * direction[2]
        return (x ** 2 + z ** 2) <= abs(self.radius)

    def intersect_caps(self, origin, direction):
        if self.closed == False or abs(direction[1]) < 0.0001: #epsilon = 0.0001
            return None

        t_lower = (self.center[1] - origin[1]) / direction[1]
        if self.check_cap(origin, direction, t_lower):
            hit = sum(origin, mul(direction, t_lower))
            normal = norm(sub(hit, self.center))

            return Intersect(distance = t_lower,
                             point = hit,
                             normal = normal,
                             texCoords = None,
                             sceneObject = self)

        t_upper = ((self.center[1] + self.height) - origin[1]) / direction[1]
        if self.check_cap(origin, direction, t_upper):
            hit = sum(origin, mul(direction, t_upper))
            normal = norm(sub(self.center,hit))

            return Intersect(distance = t_upper,
                             point=hit,
                             normal=normal,
                             texCoords = None,
                             sceneObject = self)

        return None
        

