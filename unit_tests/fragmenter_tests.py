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

import unittest
import fragmenter as frag

# Try to import both from klayout.db (PyPI klayout module) or
# pya (inside KLayout)
try:
  from klayout.db import Edge, Polygon, Vector, Point, Box, Region
except ImportError:
  from pya import Edge, Polygon, Vector, Point, Box, Region


# Unit tests for Fragments and Fragment class

class TestFragmenter(unittest.TestCase):

  def test_basic1(self):

    poly = Polygon(Box(0, 0, 1000, 500))
    fragments = frag.Fragments(poly, 300)
    self.assertEqual(repr(fragments), "(0,0;0,500),(0,500;350,500),(350,500;650,500),(650,500;1000,500),(1000,500;1000,0),(1000,0;650,0),(650,0;350,0),(350,0;0,0)")

    poly = fragments.to_polygon()
    self.assertEqual(str(poly), "(0,0;0,500;1000,500;1000,0)")

  def test_basic2(self):

    poly = Polygon(Box(0, 0, 500, 200))
    fragments = frag.Fragments(poly, 300)
    self.assertEqual(repr(fragments), "(0,0;0,200),(0,200;500,200),(500,200;500,0),(500,0;0,0)")

    poly = fragments.to_polygon()
    self.assertEqual(str(poly), "(0,0;0,200;500,200;500,0)")

  def test_lshaped_polygon(self):

    r = Region()
    r.insert(Box(0, 0, 1000, 500))
    r.insert(Box(0, 0, 500, 1000))
    r.merge()

    fragments = frag.Fragments(r[0], 300)
    self.assertEqual(repr(fragments), "(0,0;0,350),(0,350;0,650),(0,650;0,1000),(0,1000;500,1000),(500,1000;500,500),(500,500;1000,500),(1000,500;1000,0),(1000,0;650,0),(650,0;350,0),(350,0;0,0)")

    poly = fragments.to_polygon()
    self.assertEqual(str(poly), str(r[0]))

    # apply alternating shifts
    s = 10
    for ff in fragments.fragments():
      for f in ff:
        f.move(s)
        s = -s
    
    poly = fragments.to_polygon()
    self.assertEqual(str(poly), "(350,-10;350,10;-10,10;-10,350;10,350;10,650;-10,650;-10,990;510,990;510,490;1010,490;1010,10;650,10;650,-10)")

  def test_polygon_with_hole(self):

    r = Region()
    r.insert(Box(0, 0, 1000, 1000))
    r -= Region(Box(250, 250, 700, 700))

    fragments = frag.Fragments(r[0], 300)
    self.assertEqual(repr(fragments), "(0,0;0,350),(0,350;0,650),(0,650;0,1000),(0,1000;350,1000),(350,1000;650,1000),(650,1000;1000,1000),(1000,1000;1000,650),(1000,650;1000,350),(1000,350;1000,0),(1000,0;650,0),(650,0;350,0),(350,0;0,0);(250,250;700,250),(700,250;700,700),(700,700;250,700),(250,700;250,250)")

    poly = fragments.to_polygon()
    self.assertEqual(str(poly), str(r[0]))

    # apply alternating shifts
    s = 10
    for ff in fragments.fragments():
      for f in ff:
        f.move(s)
        s = -s
    
    poly = fragments.to_polygon()
    self.assertEqual(str(poly), "(350,-10;350,10;-10,10;-10,350;10,350;10,650;-10,650;-10,990;350,990;350,1010;650,1010;650,990;1010,990;1010,650;990,650;990,350;1010,350;1010,10;650,10;650,-10/240,260;710,260;710,690;240,690)")

  def test_triangle(self):

    pts = [ Point(0, 0), Point(500, 500), Point(500, 0) ]
    poly_in = Polygon(pts)

    fragments = frag.Fragments(poly_in, 300)
    self.assertEqual(repr(fragments), "(0,0;250,250),(250,250;500,500),(500,500;500,0),(500,0;0,0)")

    poly = fragments.to_polygon()
    self.assertEqual(str(poly), str(poly_in))
    
    # apply alternating shifts
    s = 10
    for ff in fragments.fragments():
      for f in ff:
        f.move(s)
        s = -s
    
    poly = fragments.to_polygon()
    self.assertEqual(str(poly), "(-4,10;243,257;257,243;510,496;510,10)")


if __name__ == '__main__':
  unittest.main()

