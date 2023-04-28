import pytest
from bs4 import BeautifulSoup

import bufet

GOOGLE_URL = 'https://www.google.com/'


@pytest.mark.asyncio
async def test_get_request():
    """
    Test asynchronous get request.
    """
    soup = await bufet.get(GOOGLE_URL)
    assert isinstance(soup, BeautifulSoup)


@pytest.fixture
def product():
    html = ('<p class="product-name">Піца</p>'
            '<p class="price">UAH 75</p>'
            '<p class="price weight">70 мг</p>')
    return BeautifulSoup(html, 'lxml')


def test_get_product_info(product: BeautifulSoup):
    """
    Test extract information about one product.
    """
    product_info = bufet.get_product_info(product)
    assert product_info == bufet.BufetProduct('Піца', 'UAH 75', '70 мг')


@pytest.fixture
def paragraph():
    html = '<p class="name">John</p>'
    return BeautifulSoup(html, 'lxml')


def test_get_product_field(paragraph: BeautifulSoup):
    """
    Test get specific field from product and perform if-exists validation.
    """
    name = bufet._get_product_field(paragraph, 'name')
    assert name == 'John'

    age = bufet._get_product_field(paragraph, 'age')
    assert age == ''
