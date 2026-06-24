import pytest
from data_get_and_processing.museum_data_req import *

def test_create_urls():
    country_name = "France"
    test_dict = create_urls(country_name)
    assert len(test_dict) == 3

