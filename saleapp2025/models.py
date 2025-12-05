from datetime import datetime
import json
from sqlalchemy import Column, ForeignKey, Integer, Float, String, Text, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship, backref
from saleapp2025 import db, app
from flask_login import UserMixin
from enum import Enum as RoleEnum

class UserEnum(RoleEnum):
    USER = 1
    ADMIN = 2

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name

class User(Base, UserMixin):
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(300), default="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRslua8fWuMCfP9XtGNcjRsmPNpmvDgncKGOQ&s",nullable=False)
    role = Column(Enum(UserEnum), nullable=False, default=UserEnum.USER)

class Category(Base):
    products = relationship("Product", backref="category", lazy=True)


class Product(Base):
    image = Column(String(300),
                   default="https://cdn2.cellphones.com.vn/insecure/rs:fill:358:358/q:90/plain/https://cellphones.com.vn/media/catalog/product/t/e/text_d_i_7_36.png")
    price = Column(Float, default=0.0)
    cate_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    description = Column(Text, nullable=False, default="Chưa có mô tả")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        # c1 = Category(name="Laptop")
        # c2 = Category(name="Mobile")
        # c3 = Category(name="Tablet")

        # db.session.add_all([c1, c2, c3])

        # db.session.commit()

        with open("D:/CNPM/SaleApp2025/data/category.json", encoding="utf-8") as f:
            category = json.loads(f.read())
            for c in category:
                db.session.add(Category(**c))
            db.session.commit()

        with open("D:/CNPM/SaleApp2025/data/product.json", encoding="utf-8") as f:
            products = json.load(f)
            for p in products:
                db.session.add(Product(**p))
            db.session.commit()

        import hashlib
        u = User(name="User", username="user", password=hashlib.md5("123456".encode("utf-8")).hexdigest())
        db.session.add(u)
        db.session.commit()
