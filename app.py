from flask import Flask, jsonify, request
import json

from auth.auth import check_user_pwd, wrap_data
from db.database import init_db, db_session, engine, PRODUCT_PER_PAGE
from db.models import Product
from business.operation import get_pro_detail_by_id, get_orders_by_id, row_proxy2dict, new_order, new_user, pay_order

app = Flask(__name__)

POST = 'POST'
CODE_SUCCESS = 1
CODE_FAIL = 0

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=[POST])
def login():
    print(request.form)
    user = request.form['userName']
    pwd = request.form['password']

    token = check_user_pwd(user, pwd)

    reps = wrap_data(
        CODE_SUCCESS, {'token': token}
                     )
    return reps


@app.route('/products/page/<page>')
def get_products(page):
    page = int(page)
    limit = PRODUCT_PER_PAGE
    offset = (page-1) * PRODUCT_PER_PAGE
    exp = "select * from products limit %d offset %d;"%(limit, offset)
    res = engine.execute(exp)
    pros = []
    for item in res:
        pros.append(row_proxy2dict(item))
    payload = {'products':pros, 'total_page':2}
    return wrap_data(CODE_SUCCESS, payload)


@app.route('/products/<pro_id>')
def get_product_detail(pro_id):
    product:Product = get_pro_detail_by_id(pro_id)
    return product


@app.route('/orders/<user_id>')
def get_user_orders(user_id):
    orders = get_orders_by_id(user_id)
    return jsonify(orders)

@app.route('/orders', methods=[POST])
def create_order():
    print(request.form)
    new_order(request.form)
    return ''

# 单笔交易
@app.route('/orders/<orderid>', methods=[POST])
def payorder(orderid):
    # 这里合理是要做检查的
    pay_order(orderid)
    return ''

@app.route('/orders/pay', methods=[POST])
def payorders():
    # 这里合理是要做检查的
    orders = json.loads(request.form['orders'])
    print(orders)
    for orderid in orders:
        pay_order(int(orderid))
    return ''

@app.route('/users', methods=[POST])
def  create_user():
    print(request.form)
    succ = new_user(request.form)
    if succ: return wrap_data(CODE_SUCCESS)
    else: return wrap_data(CODE_FAIL, None,
                           '该用户名好像已经被使用过了/(ㄒoㄒ)/~~')

if __name__ == '__main__':
    app.run()


@app.cli.command("init-db")
def create_db():
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()