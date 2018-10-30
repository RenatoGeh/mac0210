import math

import pyglet
import pyglet.text as text
from pyglet.window import mouse
from pyglet.window import key
from pyglet.gl import *

import numpy as np

import utils
from label import Label
from bezier import Bezier

WIDTH = 1280
HEIGHT = 720

class Frame(pyglet.window.Window):
  elements = None
  pre_bezier = None

  label = None
  selected = None

  pres_mode = False

  measure_dist = False
  bezier_degree = 3

  cx, cy = 0, 0
  m = None

  def __init__(self):
    super(Frame, self).__init__()
    self.set_size(WIDTH, HEIGHT)
    scr = pyglet.window.get_platform().get_default_display().get_default_screen()

    self.set_size(WIDTH, HEIGHT)
    self.set_location(int((scr.width-WIDTH)/2), int((scr.height-HEIGHT)/2))
    self.set_caption("EP1 - MAC0210 - Curvas de Bezier")

    self.elements = []
    self.pre_bezier = []
    self.label = Label()

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

  def on_draw(self):
    self.clear()
    glClear(GL_COLOR_BUFFER_BIT)
    for e in self.elements:
      glPushAttrib(GL_CURRENT_BIT)
      e.draw()
      glPopAttrib(GL_CURRENT_BIT)
    n_pre_bezier = len(self.pre_bezier)
    if n_pre_bezier > 0:
      glPushAttrib(GL_CURRENT_BIT)
      glColor3f(0, 0, 1.0)
      for i in range(n_pre_bezier-1):
        utils.draw_circle(self.pre_bezier[i], 5, 10)
      glColor3f(0, 1.0, 0)
      utils.draw_circle(self.pre_bezier[-1], 5, 10)
      glPopAttrib(GL_CURRENT_BIT)
    if self.measure_dist and self.m is not None:
      glPushAttrib(GL_CURRENT_BIT)
      glColor3f(0.7, 0.7, 0.7)
      glBegin(GL_LINES)
      glVertex2f(self.cx, self.cy)
      glVertex2f(self.m[0], self.m[1])
      glEnd()
      glPopAttrib(GL_CURRENT_BIT)
    self.label.draw()

  def _select(self, e):
    if e != self.selected and self.selected is not None:
      self.selected.sel_vtx = None
      self.selected.active = False
    self.selected = e
    self.selected.active = True

  def on_mouse_press(self, x, y, button, mods):
    self.cx, self.cy = x, y
    if button == mouse.LEFT:
      if len(self.elements) > 0:
        # First check if clicked on vertices themselves.
        s = False
        for e in self.elements:
          v = e.in_range(x, y)
          if v is not None:
            self._select(e)
            self.sel_vtx = v
            s = True
            break
        if not s:
          min, imin, pmin = math.inf, 0, None
          for i, e in enumerate(self.elements):
            pm, d = e.distance(x, y)
            if d < min:
              min, imin = d, i
              pmin = pm
          self.m = pmin
          nsel = self.elements[imin]
          self._select(nsel)
          self.label.set_dist(math.sqrt(min))

  def on_mouse_release(self, x, y, button, mods):
    if self.selected is not None:
      self.selected.mouse_pressed(x, y, button, mods)
    if button == mouse.RIGHT:
      if len(self.pre_bezier) >= self.bezier_degree:
        p = [np.array(self.pre_bezier[i]) for i in range(self.bezier_degree)]
        p.append(np.array((x, y)))
        self.elements.append(Bezier(*p, degree=self.bezier_degree))
        self.pre_bezier = []
        self.label.set_pre(0)
        self.label.set_bezier(len(self.elements))
      else:
        self.pre_bezier.append((x, y))
        self.label.set_pre(len(self.pre_bezier))

  def on_mouse_drag(self, x, y, dx, dy, buttons, mods):
    if self.selected is not None:
      self.selected.mouse_dragged(x, y, dx, dy, buttons, mods)

  def on_mouse_motion(self, x, y, dx, dy):
    pass

  def on_key_press(self, sym, mods):
    if sym == key.P:
      self.pres_mode = not self.pres_mode
      self.label.set_pres_mode(self.pres_mode)
      for e in self.elements:
        e.hide = self.pres_mode
    elif sym == key.D:
      self.measure_dist = not self.measure_dist
      self.label.set_dist_mode(self.measure_dist)
    elif sym == key.G:
      self.bezier_degree = 2 + (self.bezier_degree + 1) % 2 # switch between 2 and 3
      self.label.set_bezier_deg(self.bezier_degree)
    elif self.selected is not None and sym == key.TAB:
      self.selected.cycle_vertex()

  def start(self):
    glClearColor(255, 255, 255, 1.0)
    glColor3i(0, 0, 0)
    pyglet.app.run()

