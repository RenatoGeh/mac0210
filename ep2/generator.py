import sys

import numpy as np
import numpy.random

if len(sys.argv) != 5:
  print("Usage: " + sys.argv[0] + " filename sdv n m")
  print("  filename - file name to save to")
  print("  sdv      - gaussian standard deviation to sample with")
  print("  n        - number of samples to generate")
  print("  m        - max value for samples")
  sys.exit(1)

fname, sdv = sys.argv[1], float(sys.argv[2])
n, m = int(sys.argv[3]), int(sys.argv[4])

mu = m/2
G = []
for i in range(n):
  mu = np.random.normal(mu, sdv)
  if mu > m:
    mu = mu - 2*sdv
  if mu < 0:
    mu = mu + 2*sdv
  G.append([i, mu])

np.savetxt(fname, G, delimiter=" ")
