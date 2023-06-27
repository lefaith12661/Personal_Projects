# import functions from project.py
from project import check_string, check_city, get_clothes_rec
# import pytest to test ValueError cases
import pytest


def main():
    test_check_string()
    test_get_clothes_rec()
    test_check_city()

def test_check_string():
    assert check_string("New York") == "New York"
    with pytest.raises(ValueError):
        check_string("1234")

def test_check_city():
    assert check_city("New York") == "New York"
    with pytest.raises(ValueError):
        check_city("Seoul")

def test_get_clothes_rec():
    assert get_clothes_rec(40) == "Thick sweaters, a winter jacket, scraf, winter gloves, and insulated boots."
    assert get_clothes_rec(80) == "Airy cotton or silk tops, shorts or pants made of light materials, and sneakers or any open-toed shoes."


if __name__ == "__main__":
    main()