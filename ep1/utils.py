import math
import numpy as np
from pyglet.gl import *

DEG2RAD = np.pi/180

# Distance _squared_ from a line segment r=(p0, p1) to a point q.
def dist_seg(p0, p1, q):
  d = np.sum((p0-p1)**2)
  if d == 0:
    return np.sum((q-p0)**2)
  t = max(0, min(1, np.dot(q-p0, p1-p0)/d))
  proj = p0+t*(p1-p0)
  return np.sum((q-proj)**2)

# Compares points p0 and p1 to q. Returns the minarg distance. Either p0 or p1.
def min_pts(p0, p1, q):
  d = np.sum((p0-q)**2)
  e = np.sum((p1-q)**2)
  if d < e:
    return p0
  return p1

# Returns whether a rectangle (p0, p1) contains a point q.
def contains_pt(p0, p1, q):
  return q[0] >= p0[0] and q[0] <= p1[0] and q[1] <= p0[1] and q[1] >= p1[1]

# Draws a circle with radius r, center p and number of points n.
def draw_circle(p, r, n):
  glBegin(GL_TRIANGLE_FAN)
  glVertex2f(p[0], p[1])
  k = 2*math.pi/n
  theta = 0
  for i in range(n):
    qx = p[0] + r*math.sin(theta)
    qy = p[1] + r*math.cos(theta)
    glVertex2f(qx, qy)
    theta += k
  glVertex2f(p[0], p[1]+r)
  glEnd()
