import asyncio
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup

BUFET_URL = 'https://bufet.ua/menyu/'


@dataclass
class BufetProduct:
    """
    Entity to store bufet product data.
    """
    name: str
    price: str
    weight: str


async def get(url: str) -> BeautifulSoup:
    """
    Perform asynchronous http get request.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            return BeautifulSoup(html, 'lxml')
        

async def extract_menu():
    """
    Extract menu products from html document.
    """
    soup = await get(BUFET_URL)
    menu = soup.find_all(class_='span3')

    products = get_products_from_menu(menu)
    print(*products, sep='\n')


def get_products_from_menu(menu: BeautifulSoup) -> list[BufetProduct]:
    """
    Extract products information from menu section.
    """
    return [get_product_info(product) for product in menu]


def get_product_info(product: BeautifulSoup) -> BufetProduct:
    """
    Extract information about one product.
    """
    name = _get_product_field(product, 'product-name').strip()
    price = _get_product_field(product, 'price')
    weight = _get_product_field(product, 'price weight')

    return BufetProduct(name, price, weight)


def _get_product_field(item: BeautifulSoup, class_: str) -> str:
    """
    Get specific field from product and perform if-exists validation.
    """
    field = item.find(class_=class_)

    if field is None:
        return ''
    return field.text


if __name__ == '__main__':
    asyncio.run(extract_menu())
