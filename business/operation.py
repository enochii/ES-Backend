from db.database import db_session
from db.models import Order, Product, User
import json

# 订单只有两种状态
ORDER_UNPAID = 0
ORDER_PAID = 1

PROID = 'proid'
NAME = 'name'
PRICE = 'price'
PICTURE = 'picture'
NUM = 'num'
PRO_LABELS = ['proid', 'name', 'price', 'picture', 'num']
ORDER_ID = 'orderid'
USER_ID = 'userid'
ORDER_STATE = 'state'
STOCK = 'stock'
PASSWORD = 'password'
USERNAME = 'userName'
MAIL = 'mail'

def query_product(pro_id):
    """
     从数据库获取一个 Product
    :param pro_id:
    :return:
    """
    return Product.query.filter(Product.proid == pro_id).first()


def get_orders_by_id(user_id):
    """
    根据用户 id 获取对应的订单信息
    :param user_id:
    :return:
    """
    orders = Order.query.filter(Order.userid == user_id).all()
    dtos = [order2dict(order) for order in orders]
    return dtos


def row_proxy2dict(item):
    """
    为了分页 只能用原生 sql
    需要去读 row proxy 对象
    其实甚至还比 ORM 方便
    :param item:
    :return:
    """
    ret = {}
    for lab in PRO_LABELS:
        ret[lab] = item[lab]
    return ret

def product2dict(pro: Product, ret = None):
    if ret is None:
        ret = {}
    ret[PROID] = pro.proid
    ret[NAME] = pro.name
    ret[PRICE] = float(pro.price)
    ret[PICTURE] = pro.picture
    ret[STOCK] = pro.num
    return ret

def get_pro_detail_by_id(pro_id):
    """
    根据 pro_id 获取产品详细信息
    :param pro_id:
    :return:
    """
    product = query_product(pro_id)
    return  product2dict(product)


def order2dict(order: Order):
    ret = {}
    ret[ORDER_ID] = order.orderid
    ret[PROID] = order.proid
    ret[USER_ID] = order.userid
    ret[ORDER_STATE] = order.state
    # 需要到数据库取 该产品的数据
    product = query_product(order.proid)
    product2dict(product, ret)
    return ret


def new_order(form):
    order = Order(form[PROID], form[NUM], form[USER_ID])
    print(order)
    id = db_session.add(order)
    print(id)
    id = db_session.commit()
    print(id)


def new_user(form):
    user = User(form[USERNAME], form[PASSWORD], form[MAIL])
    db_session.add(user)
    db_session.commit()