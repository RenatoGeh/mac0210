import sys

from frame import *
from dataset import Dataset

def run():
  if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " data l")
    print("  data - dataset file")
    print("  l    - lambda constant for L2")
    sys.exit(1)

  win = Frame(Dataset(sys.argv[1]), float(sys.argv[2]))
  win.start()

if __name__ == "__main__":
  run()
