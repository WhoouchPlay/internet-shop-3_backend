from uuid import uuid4

from requests_html import HTMLSession

from src.database.models import Product
from src.database.base import db


URL = "https://rozetka.com.ua/ua/mobile-phones/c80003/"


def get_products(url: str = URL):
    session = HTMLSession()
    response = session.get(url)

    prods_url = response.html.xpath('//a[@class="ng-star-inserted" and span[@class="goods-tile__title ng-star-inserted"]]/@href')
    for prod_url in prods_url:
        save_product(prod_url)


def save_product(url):
    session = HTMLSession()
    response = session.get(url)

    name = response.html.xpath('//p[@class="title__font ng-star-inserted"]/text()')[0]
    price = response.html.xpath('//p[contains(@class, "product-price__big")]/text()')[0].replace(u"\xa0", "")
    img_url = response.html.xpath('//rz-gallery-main-content-image/img[@class="image"]/@src')[0]
    description = response.html.xpath(
        '(\
            //rz-rich-content[@class="d-block mt-6 empty-none ng-star-inserted"]|\
            //rz-text-content[@class="mt-6 empty-none ng-star-inserted"]|\
            //rz-if-in-view[@class="lazy-load-container ng-star-inserted"])\
            //text()'
        )
    description = "".join(description)

    product = Product(
        id=uuid4().hex,
        name=name,
        price=price,
        img_url=img_url,
        description=description
    )

    db.session.add(product)
    db.session.commit()

