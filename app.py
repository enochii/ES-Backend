from flask import Flask, jsonify, request

from auth.auth import check_user_pwd, wrap_data, CODE_SUCCESS
from db.database import init_db, db_session
from db.models import Product

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    user = request.form['userName']
    pwd = request.form['password']

    token = check_user_pwd(user, pwd)

    reps = wrap_data(
        CODE_SUCCESS, {'token': token}
                     )
    return jsonify(reps)


@app.route('/products/page/<page>')
def get_products(page):
    page = int(page)
    return ''


if __name__ == '__main__':
    app.run()


@app.cli.command("init-db")
def create_db():
    from db.models import User, Product, Order
    init_db()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()