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

ORDER_ID = 'orderid'
USER_ID = 'userid'
ORDER_STATE = 'state'
STOCK = 'stock'
PASSWORD = 'password'
USERNAME = 'username'
MAIL = 'mail'
DESC = 'descr'
PRO_LABELS = [PROID, NAME, PRICE, PICTURE, NUM, DESC]


def query_product(pro_id):
    """
     从数据库获取一个 Product
    :param pro_id:
    :return:
    """
    return Product.query.filter(Product.proid == pro_id).first()

def query_order(order_id):
    return Order.query.filter(Order.orderid == order_id).first()

def query_orders(userid):
    return Order.query.filter(Order.userid == userid).all()


def get_unpaid_orders_by_id(user_id):
    """
        根据用户 id 获取未付款的订单信息
        :param user_id:
        :return:
        """
    orders = Order.query.filter(Order.userid == user_id, Order.state == 0).all()
    dtos = [order2dict(order) for order in orders]
    print(dtos)
    return dtos

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
    ret[DESC] = pro.descr
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
    ret[NUM] = order.num
    # 需要到数据库取 该产品的数据
    product = query_product(order.proid)
    product2dict(product, ret)
    return ret


def new_order(form):
    userid = int(form[USER_ID])
    if userid == -1:
        uuid = form['uuid']
        _, user = try_new_user(uuid, 'nopwd')
        userid = user.id

    order = Order(form[PROID], form[NUM], userid)
    print(order)
    db_session.add(order)
    db_session.commit()
    return order.orderid, userid

def pay_order(orderid):
    order = query_order(orderid)
    if order.state == ORDER_PAID: return False
    order.state = ORDER_PAID # 付款
    try :
        # db_session.update(order)
        db_session.commit()
    except Exception as e:
        print(e)
        return False
    return True

# 尝试创建用户，用户已存在则直接返回
def try_new_user(username, pwd):
    exist_username = User.query.filter(User.name == username).all()
    if len(exist_username) != 0:
        return False, exist_username[0]

    user:User = new_user_commit(username, pwd)
    return True, user

def new_user_commit(username, pwd) :
    user = User(username, pwd)
    db_session.add(user)
    db_session.commit()
    return user

def rm_cart(orderid):
    try :
        order = Order.query.filter(Order.orderid == orderid).first()
        print('delete %d' % order.orderid)
        db_session.delete(order)
        db_session.commit()
        return True
    except Exception as e:
        print(e)
        return str(e)

def transfer_cart(anony_id, userid):
    orders = query_orders(anony_id)
    for order in orders:
        # 易主
        order.userid = userid
        print(order.userid, userid)
    db_session.commit()