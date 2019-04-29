import unittest

from src.base import get_paths, get_file
from src.data import make_dataset as md

class TestGetData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.portfolio = ["WES", 'QBE']

        candidates = ['CUV', 'ALT', "AEF", "AGL", "COH", "BHP", "ALU", "ORG", "CSL",
                      "VAS", "WOW", "A2M", "MVF"]

        cls.portfolio.extend(candidates)

    @classmethod
    def tearDownClass(cls):
        cls.portfolio

    def test_raise_ValueError(self):
        with self.assertRaises(Exception):
            try:
                md.get_data(self.portfolio, "google")

            except ValueError:
                print("Failed successfully")

            else:
                raise Exception


    def test_upper(self):
        print(self.portfolio)
        self.assertEqual('foo'.upper(), 'FOO')

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