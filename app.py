from flask import Flask, jsonify, request
import json

from flask_cors import CORS

from auth.auth import check_user_pwd, wrap_data
from db.database import init_db, db_session, engine, PRODUCT_PER_PAGE
from db.models import Product
from business.operation import get_pro_detail_by_id, get_orders_by_id, row_proxy2dict, new_order, try_new_user, \
    pay_order, \
    get_unpaid_orders_by_id, rm_cart, USERNAME, PASSWORD, transfer_cart

app = Flask(__name__)

# 跨域
CORS(app, supports_credentials=True)

POST = 'POST'
CODE_SUCCESS = 1
CODE_FAIL = 0

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=[POST])
def login():
    print(request.form)
    form = request.form
    user = form['username']
    pwd = form['password']
    uu_userid = form['userid']
    print(form)

    succ, payload = check_user_pwd(user, pwd)

    if succ is False:
        return wrap_data(CODE_FAIL, None, payload)
    # success
    transfer_cart(uu_userid, payload['userid'])
    return wrap_data(
        CODE_SUCCESS, payload
    )


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
    try:
        product = get_pro_detail_by_id(pro_id)
        print(product)
        return wrap_data(CODE_SUCCESS, product)
    except Exception as e:
        return wrap_data(CODE_FAIL, None, e)


@app.route('/orders/<user_id>')
def get_user_orders(user_id):
    orders = get_orders_by_id(user_id)
    # print(type(orders), type(orders))
    return wrap_data(CODE_SUCCESS, {'orders': orders})


@app.route('/orders/unpaid/<user_id>')
def get_user_unpaid_orders(user_id):
    orders = get_unpaid_orders_by_id(user_id)
    # print(type(orders), type(orders))
    return wrap_data(CODE_SUCCESS, {'orders': orders})


@app.route('/orders', methods=[POST])
def create_order():
    print(request.form)
    orderid, userid = new_order(request.form)
    # uuid 可能需要注册匿名用户
    return wrap_data(CODE_SUCCESS, {'orderid': orderid, 'userid': userid})

# 单笔交易
@app.route('/orders/<orderid>', methods=[POST])
def payorder(orderid):
    # 这里合理是要做检查的
    pay_order(orderid)
    return ''


@app.route('/orders/<orderid>', methods=['DELETE'])
def rmorder(orderid):
    # 这里合理是要做检查的
    succ = rm_cart(orderid)
    if succ is True: return wrap_data(CODE_SUCCESS)
    else: return wrap_data(CODE_FAIL,msg= succ + '😚')


@app.route('/orders/pay', methods=[POST])
def payorders():
    # 这里合理是要做检查的
    try:
        orders = json.loads(request.form['orders'])
        print(orders)
        for orderid in orders:
            pay_order(int(orderid))
        return wrap_data(CODE_SUCCESS)
    except Exception as e:
        print(e.with_traceback())
        return wrap_data(CODE_FAIL, None, str(e))

@app.route('/users', methods=[POST])
def  create_user():
    print(request.form)
    form = request.form
    username, pwd = form[USERNAME], form[PASSWORD]
    succ, user = try_new_user(username, pwd)
    if succ:
        print(user.id)
        return wrap_data(CODE_SUCCESS, {'username': user.name, 'password': user.pwd, 'userid': user.id})
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