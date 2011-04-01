# BEGIN_COPYRIGHT
# END_COPYRIGHT
import unittest
from bl.core.utils.pspawner import ProcessSpawner


class TestBuildCmdLine(unittest.TestCase):

  EXE = "/bin/head"

  def setUp(self):
    self.wrapper = ProcessSpawner(self.EXE)
    self.wrapper.add_opt_mapper("head.nlines", "-n")
    self.wrapper.add_opt_mapper("head.verbose", "-v")
    # dummy opts
    self.wrapper.add_opt_mapper("head.foo", "-f")
    self.wrapper.add_opt_mapper("head.bar", "-b")
    self.wrapper.add_opt_mapper("head.multi", "-m")
    self.wrapper.add_opt_mapper("head.testsep", "--testsep", sep="=")


  def __run(self, args, opts, expected_cmd_line, wrapper=None):
    if wrapper is None:
      wrapper = self.wrapper
    cmd_line = wrapper.build_cmd_line(args, opts)
    expected_cmd_line = expected_cmd_line.split()
    self.assertEqual(cmd_line, expected_cmd_line)

  def test_basic(self):
    self.__run([], {}, self.EXE)

  def test_args(self):
    self.__run(["a", "b"], {}, "%s a b" % self.EXE)

  def test_opt_with_val(self):
    arg = "foo"
    nlines = 3
    opts = {"head.nlines": nlines}
    self.__run([arg], opts, "%s -n %d %s" % (self.EXE, nlines, arg))

  def test_default_type(self):
    arg = "foo"
    x, y = "X", "Y"
    opts = {"head.foo": x, "head.bar": y}
    self.__run([arg], opts, "%s -f %s -b %s %s" % (self.EXE, x, y, arg))

  def test_ignore_None(self):
    arg = "foo"
    opts = {"head.nlines": None}
    self.__run([arg], opts, "%s %s" % (self.EXE, arg))

  def test_switch(self):
    arg = "foo"
    for verbose in False, True:
      opts = {"head.verbose": verbose}
      expected_cmd_line = str(self.EXE)
      if verbose:
        expected_cmd_line += " -v"
      expected_cmd_line += " %s" % arg
      self.__run([arg], opts, expected_cmd_line)

  def test_multi(self):
    arg = "foo"
    values = ["a=A", "b=B"]
    opts = {"head.multi": values}
    self.__run([arg], opts, "%s -m %s -m %s %s" % (
               (self.EXE,) + tuple(values) + (arg,)))

  def test_sep(self):
    arg = "foo"
    val = "X"
    opts = {"head.testsep": val}
    self.__run([arg], opts, "%s --testsep=%s %s" % (self.EXE, val, arg))


def load_tests(loader, tests, pattern):
  test_cases = (TestBuildCmdLine,)
  suite = unittest.TestSuite()
  for tc in test_cases:
    suite.addTests(loader.loadTestsFromTestCase(tc))
  return suite


if __name__ == '__main__':
  suite = load_tests(unittest.defaultTestLoader, None, None)
  runner = unittest.TextTestRunner(verbosity=2)
  runner.run(suite)
