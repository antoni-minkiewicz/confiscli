import io
import sys
import unittest

from cli import CLI


class TestCli(unittest.TestCase):
    def test_parse_arguments(self):
        argv1 = []
        cli_1 = CLI()

        text_trap = io.StringIO()
        sys.stdout = text_trap

        with self.assertRaises(SystemExit):
            cli_1.parse_arguments(argv1)
            self.assertEqual(text_trap.get_value(),
                             "usage: _jb_unittest_runner.py [-h] [--target target file] source file")



class TestMain(unittest.TestCase):
    def test_if_no_params_fails(self):
        argument_parser = CLI()
        test_args = []
        with self.assertRaises(SystemExit):
            argument_parser.parse_arguments(test_args)


    def test_if_no_guide_executes_default_conversion(self):
        argument_parser = CLI()
        test_args = ["testing-materials/simple.confis.kts.pdf"]
        argument_parser.parse_arguments(test_args)

    def test_if_guide_executes_guided_conversion(self):
        argument_parser = CLI()
        test_args = ["testing-materials/simple.confis.kts.pdf", "-g", "hello"]
        argument_parser.parse_arguments(test_args)

if __name__ == '__main__':
    unittest.main()
