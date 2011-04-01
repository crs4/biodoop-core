# this should only be used to perform a quick check for missing
# imports and similar macroscopic errors: try*.py modules are not
# meant to be used for automated testing.

import sys, os


def get_try_scripts():
  scripts = []
  D = os.path.dirname(os.path.abspath(__file__))
  for root, dirs, files in os.walk(D):
    for fn in files:
      if fn.startswith("try") and fn.endswith(".py"):
        path = os.path.join(root, fn)
        yield path


if __name__ == "__main__":
  for i, s in enumerate(get_try_scripts()):
    print "\n* RUNNING %r" % s
    os.system("%s %s" % (sys.executable, s))
  print "\n* RAN %d scripts" % (i+1)
