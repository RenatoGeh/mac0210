import pyglet
from pyglet.gl import *
import pyglet.text as text

class Label:
  txt_bezier = None
  n_bezier = None

  txt_pre_pts = None
  n_pre_pts = None

  txt_dist_mode = None
  dist_mode = None

  text = None
  in_labels = None

  def __init__(self):
    self.n_bezier = 0
    self.n_pre_pts = 0
    self.text = ""
    self.in_label = text.Label(self.text, font_name="Times New Roman", font_size=12,
                               x=10, y=25, anchor_y="center", color=(0, 0, 0, 255), multiline=True,
                               width=500)
    self.retext()

  def retext(self):
    self.txt_bezier = "Number of bezier curves: %d" % (self.n_bezier)
    self.txt_pre_pts = "Pre-bezier points: %d" % (self.n_pre_pts)
    self.txt_dist_mode = "Distance debug mode: " + str(self.dist_mode)
    self.text = self.txt_bezier + "\n" + self.txt_pre_pts
    self.in_label.text = self.text

  def set_bezier(self, n):
    self.n_bezier = n
    self.retext()

  def set_pre(self, n):
    self.n_pre_pts = n
    self.retext()

  def set_dist_mode(self, m):
    self.dist_mode = m
    self.retext()

  def draw(self):
    glColor3f(0, 0, 0)
    self.in_label.draw()
