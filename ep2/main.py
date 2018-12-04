import sys

from frame import *
from dataset import Dataset

def run():
  if len(sys.argv) != 4:
    print("Usage: " + sys.argv[0] + " data n l")
    print("  data - dataset file")
    print("  n    - bounds for t")
    print("  l    - lambda constant for L2")
    sys.exit(1)

  win = Frame(Dataset(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]))
  win.start()

if __name__ == "__main__":
  run()
