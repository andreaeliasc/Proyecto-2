from lib import *
from dataclasses import dataclass
from math import *


WHITE = color(255, 255, 255)

class Light(object):
  def __init__(self, position=V3(0,0,0), intensity=1):
    self.position = position
    self.intensity = intensity

class Material(object):
  def __init__(self, diffuse=WHITE, albedo=(1, 0, 0, 0), spec=0, refractive_index=1):
    self.diffuse = diffuse
    self.albedo = albedo
    self.spec = spec
    self.refractive_index = refractive_index

class Intersect(object):
  def __init__(self, distance=0, point=None, normal=None):
    self.distance = distance
    self.point = point
    self.normal = normal

class Sphere(object):
  def __init__(self, center, radius, material):
    self.center = center
    self.radius = radius
    self.material = material

  def ray_intersect(self, orig, direction):
    L = sub(self.center, orig)
    tca = dot(L, direction)
    l = length(L)
    d2 = l**2 - tca**2
    if d2 > self.radius**2:
      return None
    thc = (self.radius**2 - d2)**1/2
    t0 = tca - thc
    t1 = tca + thc
    if t0 < 0:
      t0 = t1
    if t0 < 0:
      return None

    hit = sum(orig, mul(direction, t0))
    normal = norm(sub(hit, self.center))

    return Intersect(
      distance=t0,
      point=hit,
      normal=normal
    )
from plane import *
class Cube(object):
  def __init__(self, position, size, material):
    self.position = position
    self.size = size
    self.material = material
    self.planes = []
    halfSize = size / 2
    self.planes.append(Plane(sum(position, V3(halfSize,0,0)), V3(1,0,0), material))
    self.planes.append(Plane(sum(position, V3(-halfSize,0,0)), V3(-1,0,0), material))
    self.planes.append(Plane(sum(position, V3(0,halfSize,0)), V3(0,1,0), material))
    self.planes.append(Plane(sum(position, V3(0,-halfSize,0)), V3(0,-1,0), material))
    self.planes.append(Plane(sum(position, V3(0,0,halfSize)), V3(0,0,1), material))
    self.planes.append(Plane(sum(position, V3(0,0,-halfSize)), V3(0,0,-1), material))

  def ray_intersect(self, origin, direction):
    epsilon = 0.001
    min_boundbox = [0, 0, 0]
    max_boundbox = [0, 0, 0]

    for i in range(3):
      min_boundbox[i] = self.position[i] - (epsilon + self.size / 2)
      max_boundbox[i] = self.position[i] + (epsilon + self.size / 2)

    t = float('inf')
    intersect = None

    for plane in self.planes:
      plane_intersect = plane.ray_intersect(origin, direction)

      if plane_intersect is not None:
        if plane_intersect.point[0] >= min_boundbox[0] and plane_intersect.point[0] <= max_boundbox[0]:
          if plane_intersect.point[1] >= min_boundbox[1] and plane_intersect.point[1] <= max_boundbox[1]:
            if plane_intersect.point[2] >= min_boundbox[2] and plane_intersect.point[2] <= max_boundbox[2]:
              if plane_intersect.distance < t:
                t = plane_intersect.distance
                intersect = plane_intersect

    if intersect is None:
      return None
    return Intersect(
      distance = intersect.distance,
      point = intersect.point,
      normal = intersect.normal
    )


