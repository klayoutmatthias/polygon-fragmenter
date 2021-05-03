
# A simple polygon fragmenter framework for KLayout

Polygon fragmentation is the process of inserting points into a polygon 
contour to make the contour consist of shorter edges with a finite length.

Given you have a KLayout Polygon object, you can use the classes from
the fragmenter framework to turn a polygon into a fragmented representation,
manipulate the fragments (currently: shift) and turn the result back into
polygons.

**NOTE: this module needs Python 3!**

Here is some sample code:

```
from pya import Point, Polygon
import fragmenter as frag

# create a triangle as a sample polygon
pts = [ Point(0, 0), Point(500, 500), Point(500, 0) ]
poly_in = Polygon(pts)

# Turn the polygon into fragments with a min length of 
# 300 DBU and a max length of <600 DBU.
fragments = frag.Fragments(poly_in, 300)

# apply alternating shifts
s = 10
for ff in fragments.fragments():   # outer loop is over contours: hull (first) and holes (next)
  for f in ff:                     # inner loop is over fragments of the contours
    f.move(s)
    s = -s
    
# turn back into polygon
poly = fragments.to_polygon()
print(str(poly))
```

