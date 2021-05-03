#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#

# Try to import both from klayout.db (PyPI klayout module) or
# pya (inside KLayout)
try:
  from klayout.db import Edge, Polygon, Vector
except ImportError:
  from pya import Edge, Polygon, Vector


class Fragment(object):
  
  """
  A single polygon fragment

  A fragment is a part of a polygon edge.
  Objects of this class are generated by the Fragmenter class 
  and hold a single polygon fragment. 
  """

  def __init__(self, edge):

    """
    Creates a fragment
    """

    self.edge = edge

  def move(self, d):

    """
    Moves the fragement by the given distance

    A positive distance is to the outside, a negative distance to the inside 
    of the polygon.

    Distances are given in database units
    """

    self.edge.shift(d)


class Fragments(object):

  """
  Fragmented representation of a polygon

  All polygon objects involved need to be of KLayout's pya.Polygon type.

  This class can represent an original polygon in terms of "fragments".
  Fragments are parts of polygon edges with a finite length.
  The length of the fragments is at least the given min. length (unless the 
  polygon itself has edges with smaller length) and twice the min length max.

  Fragments can be manipulated, secifically they can be shifted.

  The fragment representation can be turned back into a polygon 
  using the "to_polygon" method.
  """

  def __init__(self, polygon, min_length):

    """
    Initializes the fragment representation from the given polygon with
    the given min. length.
    The polygon should be of pya.Polygon type and min length given in
    database units.
    """

    self._fragments = []

    contours = 1 + polygon.holes()

    for c in range(0, contours):

      fragments = []
      self._fragments.append(fragments)

      for e in polygon.each_edge(c):

        if e.length() < min_length * 2:

          fragments.append(Fragment(e))

        else:

          nmin = (e.length() // min_length) - 2
          norm = 1.0 / e.length()
          rem = (e.length() - nmin * min_length) // 2

          p = e.p1
          pp = p + e.d() * (rem * norm)
          fragments.append(Fragment(Edge(p, pp)))

          p = pp
          for i in range(0, nmin):
            pp = p + e.d() * (min_length * norm)
            fragments.append(Fragment(Edge(p, pp)))
            p = pp

          fragments.append(Fragment(Edge(p, e.p2)))

  def fragments(self):

    """
    Gets the fragments.
    This method returns a list of lists of Fragment objects.
    The first list are the fragments of the hull. 
    The following lists are the fragments of the holes.
    """

    return self._fragments

  def to_polygon(self):

    """
    Turns the fragments back into a polygon
    """

    poly = Polygon()
    poly.assign_hull(self._fragments_to_points(self._fragments[0]))
    for h in range(1, len(self._fragments)):
      poly.insert_hole(self._fragments_to_points(self._fragments[h]))

    return poly

  def __repr__(self):

    """
    Returns a string representation
    """

    return ";".join([ ",".join([ str(f.edge) for f in ff ]) for ff in self._fragments ])

  def _fragments_to_points(self, fragments):

    pts = []

    for n in range(0, len(fragments)):
      
      e = fragments[n].edge
      ebefore = fragments[n - 1].edge

      if ebefore.p2 == e.p1:
        
        # both edges connect: do nothing.
        pass 

      if e.d().vprod_sign(ebefore.d()) == 0:

        # parallel edges: create a step
        pts.append(ebefore.p2)
        pts.append(e.p1)

      else:

        # otherwise they need to intersect: compute and store the intersection point
        vp2 = e.d().vprod(ebefore.d())
        vp1 = (e.p1 - ebefore.p2).vprod(ebefore.d())
        pts.append(e.p1 - e.d() * (vp1 / vp2))
        
    return pts


