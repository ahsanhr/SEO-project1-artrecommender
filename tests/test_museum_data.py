import unittest
from unittest.mock import patch
import pandas as pd
from pandas.testing import assert_frame_equal

from data_get_and_processing.museum_data_req import *

class TestMuseumData(unittest.TestCase):
    def test_create_urls(self):
        country_name = "France"
        test_dict = create_urls(country_name)
        self.assertEqual(len(test_dict), 3)

    def test_get_chicago_works(self):
        country_name = "France"
        test_urls = create_urls(country_name)
        test_chicago_dict = get_chicago_works(test_urls['chi'])
        for k, v in test_chicago_dict.items():
            self.assertIn('https://www.artic.edu/artworks/', v[1])


    @patch('data_get_and_processing.museum_data_req.create_works_df')
    def test_create_works_df(self, mock_fetch):
        mock_dict = {
            "work_{i}": [f"Artist {i}", "http://link.com", "http://image.com"] 
            for i in range(15)
        }
        mock_fetch.return_value = mock_dict
        country_name = "France"
        test_urls = create_urls(country_name)
        result_df = create_works_df(test_urls)
        self.assertEqual(len(result_df), 10)

    
if __name__ == '__main__':
    unittest.main()
