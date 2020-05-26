# 用户


def check_user_pwd(user, pwd):
    return 'token'


def wrap_data(code, payload=None, msg='ok'):
    return \
        {
            'payload': payload,
            'code': code,
            'msg': msg
        }