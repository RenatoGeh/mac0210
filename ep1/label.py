import math

import pyglet
from pyglet.gl import *
import pyglet.text as text

class Label:
  txt_bezier = None
  n_bezier = 0

  txt_pre_pts = None
  n_pre_pts = 0

  txt_dist_mode = math.inf
  dist_mode = False

  txt_dist = None
  dist = None

  txt_bez_deg = None
  bez_deg = 3

  txt_pres_mode = None
  pres_mode = False

  text = None
  in_label = None
  cmds_label = None

  def __init__(self):
    self.text = ""
    self.in_label = text.Label(self.text, font_name="Times New Roman", font_size=12,
                               x=10, y=75, anchor_y="center", color=(0, 0, 0, 255), multiline=True,
                               width=500)
    self.retext()
    self.cmds_label = text.Label("Key and mouse commands:\n  - Mouse:\n    LMB: Selects nearest " + \
                                 "curve\n    RMB: Creates new bezier vertex\n  - Keyboard:\n    "+ \
                                 "P: presentation mode\n    D: line distance mode\n    G: " + \
                                 "change bezier degree\n    Shift+X: clear canvas\n    Del: " + \
                                 "destroy selected curve",
                                 font_name="Times New Roman", font_size=12, x=1030, y=115,
                                 anchor_y="center", color=(0, 0, 0, 255), multiline=True,
                                 width=300)

  def retext(self):
    self.txt_bezier = "Number of bezier curves: %d" % (self.n_bezier)
    self.txt_pre_pts = "Pre-bezier points: %d" % (self.n_pre_pts)
    self.txt_bez_deg = "Bezier degree: %d" % (self.bez_deg)
    self.txt_pres_mode = "Presentation mode: " + str(self.pres_mode)
    self.txt_dist_mode = "Distance debug mode: " + str(self.dist_mode)
    self.txt_dist = "Distance of curve: " + str(self.dist)
    self.text = self.txt_bezier + "\n" + self.txt_pre_pts + "\n" + self.txt_bez_deg + "\n" + \
                self.txt_pres_mode + "\n" + self.txt_dist_mode + "\n" + self.txt_dist
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

  def set_dist(self, d):
    self.dist = d
    self.retext()

  def set_bezier_deg(self, d):
    self.bez_deg = d
    self.retext()

  def set_pres_mode(self, m):
    self.pres_mode = m
    self.retext()

  def draw(self):
    if not self.pres_mode:
      glColor3f(0, 0, 0)
      self.in_label.draw()
      self.cmds_label.draw()
