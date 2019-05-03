import unittest
import pandas as pd
import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.data import make_dataset as md

DEFAULT_PORTFOLIO = ["WES", 'QBE', 'CUV', 'ALT', "AEF", "AGL", "COH", "BHP",
                     "ALU", "ORG", "CSL", "VAS", "WOW", "A2M", "MVF"]

class TestGetData(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.portfolio = DEFAULT_PORTFOLIO


    @classmethod
    def tearDownClass(cls):
        cls.portfolio


    def test_raise_ValueError(self):
        self.assertRaises(ValueError, md.get_data, self.portfolio, "google")


    def test_Output(self):
        data = md.get_data(self.portfolio, "yahoo")
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(data.shape[1], len(self.portfolio))


class TestInput_data(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.portfolio = DEFAULT_PORTFOLIO
        cls.data = md.get_data(self.portfolio, "yahoo")


    @classmethod
    def tearDownClass(cls):
        cls.portfolio
        cls.data


if __name__ == "__main__":
    unittest.main()