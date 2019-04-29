import unittest

from src.base import get_paths, get_file
from src.data import make_dataset as md

class TestGetData(unittest.TestCase):

    def setUp(self):
        portfolio = ["WES", 'QBE']

        # candidates = ['CUV', 'ALT', "AEF", "AGL", "COH", "BHP", "ALU", "ORG", "CSL",
        #               "VAS", "WOW", "A2M", "MVF"]
        #
        # portfolio.extend(candidates)


    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertEqual(portfolio, portfolio)

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == "__main__":
    unittest.main()