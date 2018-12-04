import sys

import numpy as np
import numpy.random

if len(sys.argv) != 6:
  print("Usage: " + sys.argv[0] + " filename sdv n m")
  print("  filename - file name to save to")
  print("  sdv      - gaussian standard deviation to sample with")
  print("  n        - number of samples to generate")
  print("  m        - max value for samples")
  print("  t        - number of samples per column")
  sys.exit(1)

fname, sdv = sys.argv[1], float(sys.argv[2])
n, m = int(sys.argv[3]), int(sys.argv[4])
t = int(sys.argv[5])

mu = m/2
G = []
for i in range(n):
  mu = np.random.normal(mu, sdv, t)
  for u in mu:
    if u > m:
      u = u - 2*sdv
    if u < 0:
      u = u + 2*sdv
    G.append([i, u])
  mu = np.mean(mu)

np.savetxt(fname, G, delimiter=" ")
