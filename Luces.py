from lib import *
from math import sqrt
from sphere import *

#Extraido y apaptado en base al contenido encontrado en: https://github.com/tobycyanide/pytracer/blob/master/raytracer/shapes.py
class Luces(object):
#Inicializo los atributos radio, altura, centro, material

    def __init__(self, radio, altura, center, material):
        self.radio = radio
        self.altura = altura
        self.closed = False
        self.center = center
        self.material = material

    def ray_intersect(self, origin, direccion):
        a = direccion[0] ** 2 + direccion[2] ** 2
        if abs(a) < 0.0001: #epsilon = 0.0001
            return None

        b = 2 * (
            direccion[0] * (origin[0] - self.center[0])
            + direccion[2] * (origin[2] - self.center[2])
        )
        c = (
            (origin[0] - self.center[0]) ** 2
            + (origin[2] - self.center[2]) ** 2
            - (self.radio ** 2)
        )

        discriminant = b ** 2 - 4 * (a * c)

        if discriminant < 0.0:
            return None

        t0 = (-b - sqrt(discriminant)) / (2 * a)
        t1 = (-b + sqrt(discriminant)) / (2 * a)

        if t0 > t1:
            t0, t1, t1, t0

        y0 = origin[1] + t0 * direccion[1]
        if self.center[1] < y0 and y0 <= (self.center[1] + self.altura):
            hit = sum(origin, mul(direccion,t0))
            normal = norm(sub(self.center, hit))
            return Intersect(distance = t0,
                             point = hit,
                             normal = normal
                             )

        y1 = origin[1] + t1 * direccion[1]
        if self.center[1] < y1 and y1 <= (self.center[1] + self.altura):
            hit = sum(origin, mul(direccion, t1))
            normal = norm(sub(self.center, hit))
            return Intersect(distance=t1,
                             point = hit,
                             normal = normal
            )
        return self.intersectC(origin, direccion)

    def capasVerif(self, origin, direccion, t):
        x = origin[0] + t * direccion[0]
        z = origin[2] + t * direccion[2]
        return (x ** 2 + z ** 2) <= abs(self.radio)

    def intersectC(self, origin, direccion):
        if self.closed == False or abs(direccion[1]) < 0.0001: #epsilon = 0.0001
            return None

        t_inferior = (self.center[1] - origin[1]) / direccion[1]
        if self.capasVerif(origin, direccion, t_inferior):
            hit = sum(origin, mul(direccion, t_inferior))
            normal = norm(sub(hit, self.center))
            return Intersect(distance = t_inferior,
                             point = hit,
                             normal = normal,
                             Coordenadas = None,
                             scene = self)
        t_superior = ((self.center[1] + self.altura) - origin[1]) / direccion[1]
        if self.capasVerif(origin, direccion, t_superior):
            hit = sum(origin, mul(direccion, t_superior))
            normal = norm(sub(self.center,hit))

            return Intersect(distance = t_superior,
                             point=hit,
                             normal=normal,
                             Coordenadas = None,
                             scene = self)

        return None
        

