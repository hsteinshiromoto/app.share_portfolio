import unittest
import pandas as pd
import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

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


    def test_Output(self):
        data = md.get_data(self.portfolio, "yahoo")
        self.assertIsInstance(data, pd.DataFrame)
        self.assertEqual(data.shape[1], len(self.portfolio))

if __name__ == "__main__":
    unittest.main()