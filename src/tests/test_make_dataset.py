import unittest
import pandas as pd
import numpy as np

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
        # Create data set with missing values

        # Definitions
        n_samples = 100
        cls.missing_values_tolerance = np.random.randint(10)
        data_array = np.array(range(n_samples))
        indices_with_nulls =  np.random.randint(n_samples,
                                                size=cls.missing_values_tolerance)

        cls.data_no_nulls = pd.DataFrame(data_array, columns=["Feature"])
        # Do not remove the .copy() from the data frame
        cls.data_with_nulls = cls.data_no_nulls.copy()
        cls.data_with_nulls.loc[indices_with_nulls, :] = np.nan


    @classmethod
    def tearDownClass(cls):
        cls.missing_values_tolerance
        cls.data_no_nulls
        cls.data_with_nulls


    def test_output(self):
        data_no_nulls = md.input_data(self.data_no_nulls)
        # Do not remove the .copy() from the data frame
        data_with_nulls = md.input_data(self.data_with_nulls.copy(),
                                        missing_values_tolerance=self.missing_values_tolerance)
        self.assertEqual(data_no_nulls.isnull().sum().sum(), 0)
        self.assertEqual(data_with_nulls.isnull().sum().sum(), 0)


    def test_raise_ValueError(self):
        self.assertNotEqual(self.data_with_nulls.isnull().sum().sum(), 0)
        self.assertRaises(ValueError, md.input_data, self.data_with_nulls,
                          self.missing_values_tolerance / 10)



if __name__ == "__main__":
    unittest.main()