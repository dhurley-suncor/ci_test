import pandas as pd
import unittest
from unittest.mock import patch
from functions import *

class test_dataframe_functions(unittest.TestCase):
        
    def test_remove_duplicates(self):
        
        test_df = pd.DataFrame({
            'datetime': ['2022-06-01', '2022-06-01'],
            'item': ['A', 'A'],
            'price_cad': [10, 10]
            })

        expected_rows = 1

        result = remove_duplicates(test_df)

        number_of_rows = len(result)

        self.assertEqual(expected_rows, number_of_rows)

    def test_calculate_price_usd(self):

        test_df = pd.DataFrame({
            'datetime': ['2022-06-01'],
            'item': ['A'],
            'price_cad': [10]
            })

        expected_price = 8

        result = calculate_price_usd(test_df)

        price = result.price_usd[0]

        self.assertEqual(expected_price, price)

    @patch('pandas.read_csv')
    def test_calculate_mean_price(self, read_csv):

        read_csv.return_value = pd.DataFrame({
            'datetime': ['2022-06-01', '2022-06-02', '2022-06-03'],
            'item': ['A', 'B', 'C'],
            'price_cad': [10, 20, 30]
            })

        expected_avg = 20

        result = calculate_mean_price()

        self.assertEqual(result, expected_avg)