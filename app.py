import datetime
import json
from flask import Flask, render_template, jsonify, request
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_httpauth import HTTPBasicAuthreid

from core.db import CookiesPoolRedis
from config import Config

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
@app.route('/mail/send', methods=['GET'])
# @auth.login_required
def mail_send_get():
    account = REDIS_MODEL.get_send_mail()
    return jsonify(account)

# 查询所有的keys
@app.route('/mail/send', methods=['POST'])
# @auth.login_required
def mail_send_post():
    account = request.form.get('account', None)
    password = request.form.get('password', None)
    if not all([account, password]):
        return error(msg='account or password is none')
    REDIS_MODEL.update_send_mail(account, password)
    return ok()


# 查询所有的邮件接受者
@app.route('/mail/recv', methods=['GET'])
# @auth.login_required
def mail_recv_get():
    result = REDIS_MODEL.list_all_mail_receivers()
    return jsonify(result)


# 添加一个邮件接受人
@app.route('/mail/recv', methods=['POST'])
# @auth.login_required
def mail_recv_post():
    account = request.form.get('account', None)
    if not account:
        return error(msg='account is none')
    result = REDIS_MODEL.add_mail_receiver(account)
    return ok(msg=result)

# 更新一个邮件接受人
@app.route('/mail/recv', methods=['PUT'])
# @auth.login_required
def mail_recv_put():
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

    REDIS_MODEL.update_mail_receiver(account, is_recv)
    return ok()


# 删除一个邮件接受人
@app.route('/mail/recv', methods=['DELETE'])
# @auth.login_required
def mail_recv_del():
    account = request.args.get('account', None)
    if not account:
        return error(msg='account is none')
    REDIS_MODEL.delete_mail_receiver(account)
    return ok()


def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=Config.API_SERVER_PORT)


if __name__ == '__main__':
    run()
