from typing import List
from uuid import uuid4

from src.database.models import Product, Review, User
from src.database.base import db

def get_products() -> List[Product]:
    return db.session.query(Product).all()


def get_product(prod_id: str) -> Product:
    return db.one_or_404(db.session.query(Product).where(Product.id == prod_id))


def add_product(name: str, description: str, img_url: str, price: float) -> str:
    product = Product(
        id=uuid4().hex,
        name=name,
        description=description,
        img_url=img_url,
        price=price
    )
    db.session.add(product)
    db.session.commit()
    return product.id


def update_product(prod_id: str, name: str, description: str, img_url: str, price: float):
    product = db.one_or_404(db.session.query(Product).where(Product.id == prod_id))
    product.description = description
    product.img_url = img_url
    product.price = price
    db.session.commit()
    return product.id
    


def del_product(prod_id: str):
    product = db.one_or_404(db.session.query(Product).where(Product.id == prod_id))
    db.session.delete(product)
    db.session.commit()



def add_review_by_product(prod_id: str, text: str, grade: str):
    review = Review(
        id=uuid4().hex,
        text=text,
        grade=grade
    )


    product = db.one_or_404(db.session.query(Product).where(Product.id == prod_id))
    product.reviews.append(review)
    db.session.commit()


def add_user(email: str, password: str, name: str|None = None):
    user = User(
        id=uuid4().hex,
        name=name,
        email=email,
        password=password
    )
    db.session.add(user)
    db.session.commit()
    return "Ви успішно увійшли в систему."


def get_tokens(email: str, password: str) -> dict:
    user = db.one_or_404(db.session.query(User).where(User.email == email))
    return user.get_tokens(password)


def get_user(user_id: str):
    user = db.one_or_404(db.session.query(User).where(User.id == user_id))