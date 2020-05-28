# 用户
from db.models import User


def check_user_pwd(username, pwd):
    try:
        u:User = User.query.filter(User.name == username).first()
        if u.pwd == pwd:
            return True, {'token': 'token', 'userid':u.id, 'username':u.name}
        else:
            return False, '密码好像错了哦(⊙o⊙)？'
    except Exception as e:
        return False, '操作出现异常，你真的注册了吗？'


def wrap_data(code, payload=None, msg='ok'):
    return \
        {
            'payload': payload,
            'code': code,
            'msg': msg
        }