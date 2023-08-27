# Import required modules for testing
import unittest
from unittest.mock import patch, Mock
import pandas as pd
import os

# Import your module
import data_fetchy as dfetch


class TestFetchData(unittest.TestCase):

    def assertDataFrameEqual(self, df1, df2):
        self.assertTrue(df1.equals(df2))

    @patch('data_fetchy.fetch_stock_data')  # Mock fetch_stock_data function
    @patch('data_fetchy.write_to_csv')  # Mock write_to_csv function
    def test_fetch_data(self, mock_write_to_csv, mock_fetch_stock_data):
        # Mock the output of fetch_stock_data function
        mock_fetch_stock_data.return_value = pd.DataFrame({'Date': ['2020-01-01'], 'Price': [100]})

        # Call the function to test
        dfetch.fetch_data(['AAPL'])

        # Check if the mocked functions were called
        mock_fetch_stock_data.assert_called()
        mock_write_to_csv.assert_called()

        # Extract the DataFrame argument from the mock_write_to_csv call
        called_df = mock_write_to_csv.call_args[0][0]

        # Assert that the DataFrames are equal
        expected_df = pd.DataFrame({'Date': ['2020-01-01'], 'Price': [100]})


# Unit test for the function fetch_stock_data
class TestFetchStockData(unittest.TestCase):

    def test_fetch_stock_data(self):
        # Call the function to test
        result = dfetch.fetch_stock_data('AAPL', '2020-01-01', '2021-01-01')

        # Validate the output
        self.assertTrue(result.empty)


# Unit test for the function write_to_csv
class TestWriteToCSV(unittest.TestCase):

    @patch('os.path.exists')  # Mock os.path.exists function
    @patch('pandas.DataFrame.to_csv')  # Mock to_csv function
    @patch('os.makedirs')  # Mock os.makedirs function
    def test_write_to_csv(self, mock_makedirs, mock_to_csv, mock_path_exists):
        # Mock the output of os.path.exists function
        mock_path_exists.return_value = False

        # Prepare data to pass to the function
        data = pd.DataFrame({'Date': ['2020-01-01'], 'Price': [100]})

        # Call the function to test
        dfetch.write_to_csv(data, 'AAPL_5_year_history.csv')

        # Validate if the mocked functions were called
        mock_makedirs.assert_called_with('historical-data')
        mock_to_csv.assert_called()


# Run the tests
if __name__ == '__main__':
    unittest.main()
