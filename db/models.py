from sqlalchemy import Column, Integer, String, Float
import sqlalchemy
from db.database import Base

# 用户
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    pwd = Column(String(200))

    def __init__(self, name:not None, pwd:not None,email=None):
        self.name = name
        self.pwd = pwd

        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


# 商品
class Product(Base):
    __tablename__ = 'products'
    proid = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    num = Column(Integer)
    price = Column(Float)
    picture = Column(String(200))
    descr = Column(String(400))

    def __init__(self, name:not None, price, picture):
        self.name = name
        self.price = price
        self.picture = picture
        self.num = 90

    def __repr__(self):
        return '<Product %r>' % (self.name)


# 订单
class Order(Base):
    __tablename__ = 'orders'
    orderid = Column(Integer, primary_key=True)
    proid = Column(Integer)
    num = Column(Integer)
    state = Column(Integer)
    userid = Column(Integer)

    def __init__(self, proid, num, userid):
        self.proid = proid
        self.num = num
        self.state = 0 # 刚下单
        self.userid = userid