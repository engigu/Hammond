import datetime
import json
from flask import Flask, render_template, jsonify, request
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_httpauth import HTTPBasicAuthreid

from core.db import CookiesPoolRedis
from config import Config, RedisStoreKeyConfig
from core.defined import ConfigKey

REDIS_MODEL = CookiesPoolRedis(uri=Config.BACKEND_REDIS_URI)
app = Flask(__name__)
# auth = HTTPBasicAuth()

# @auth.verify_password
# def verify_password(username, password):
#     if username in users:
#         return check_password_hash(users.get(username), password)
#     return False


def error(code=-1,  msg='inter error'):
    return jsonify({'code': code, 'msg': msg})


def ok(code=0,  msg='ok!'):
    return jsonify({'code': code, 'msg': msg})


@app.route('/')
# @auth.login_required
def index():
    return 'WELCOME TO WORLD!<br />'


# 查询所有的keys
@app.route('/send/mail_backend', methods=['GET'])
# @auth.login_required
def mail_send_get():
    account = REDIS_MODEL.get_send_mail()
    return jsonify(account)

# 查询所有的keys
@app.route('/send/mail_backend', methods=['POST'])
# @auth.login_required
def mail_send_post():
    account = request.form.get('account', None)
    password = request.form.get('password', None)
    if not all([account, password]):
        return error(msg='account or password is none')
    REDIS_MODEL.update_send_mail(account, password)
    return ok()


# 查询所有的接受者
@app.route('/recv/<ctype>', methods=['GET'])
# @auth.login_required
def recv_get(ctype):
    if ctype not in ConfigKey.keys:
        return error(msg='ctype in url is error!')
    redis_key = getattr(ConfigKey, ctype)

    result = REDIS_MODEL.list_all_receivers(redis_key=redis_key)
    return jsonify(result)


# 添加一个接受人
@app.route('/recv/<ctype>', methods=['POST'])
# @auth.login_required
def recv_post(ctype):
    if ctype not in ConfigKey.keys:
        return error(msg='ctype in url is error!')
    redis_key = getattr(ConfigKey, ctype)
    account = request.form.get('account', None)
    if not account:
        return error(msg='account is none')
    result = REDIS_MODEL.add_receiver(account=account, redis_key=redis_key)
    return ok(msg=result)


# 更新一个接受人
@app.route('/recv/<ctype>', methods=['PUT'])
# @auth.login_required
def recv_put(ctype):
    if ctype not in ConfigKey.keys:
        return error(msg='ctype in url is error!')
    redis_key = getattr(ConfigKey, ctype)

    account = request.form.get('account', None)
    is_recv = request.form.get('is_recv', None)
    if not all([account, is_recv]):
        return error(msg='account or is_recv is none')

    try:
        is_recv = int(is_recv)
        if is_recv not in [1, 0]:
            raise Exception
    except:
        return error(msg='is_recv not in [1, 0]!')

    REDIS_MODEL.update_receiver(
        account=account, is_recv=is_recv, redis_key=redis_key)
    return ok()


# 删除一个接受人
@app.route('/recv/<ctype>', methods=['DELETE'])
# @auth.login_required
def recv_del(ctype):
    if ctype not in ConfigKey.keys:
        return error(msg='ctype in url is error!')
    redis_key = getattr(ConfigKey, ctype)

    account = request.args.get('account', None)
    if not account:
        return error(msg='account is none')
    REDIS_MODEL.delete_receiver(account=account, redis_key=redis_key)
    return ok()


# 发送消息
@app.route('/notice', methods=['POST'])
# @auth.login_required
def notice():

    account = request.args.get('account', None)
    if not account:
        return error(msg='account is none')
    REDIS_MODEL.delete_receiver(account=account, redis_key=redis_key)
    return ok()


def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=Config.API_SERVER_PORT)


if __name__ == '__main__':
    run()
