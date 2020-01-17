import datetime
import json
from flask import Flask, render_template, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth

from core.db import RedisModel
from config import Config, RedisStoreKeyConfig
from core.defined import ConfigKey
from celery_senders.sender import ALL_SENDERS, send_notice

REDIS_MODEL = RedisModel(uri=Config.BACKEND_REDIS_URI)
app = Flask(__name__)
auth = HTTPBasicAuth()

USERS = {u: generate_password_hash(p) for u, p in Config.HTTP_AUTH.items()}


@auth.verify_password
def verify_password(username, password):
    if username in USERS:
        return check_password_hash(USERS.get(username), password)
    return False


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
@auth.login_required
def mail_send_get():
    account = REDIS_MODEL.get_send_mail()
    return jsonify(account)

# 查询所有的keys
@app.route('/send/mail_backend', methods=['POST'])
@auth.login_required
def mail_send_post():
    account = request.form.get('account', None)
    password = request.form.get('password', None)
    if not all([account, password]):
        return error(msg='account or password is none')
    REDIS_MODEL.update_send_mail(account, password)
    return ok()


# 查询所有的接受者
@app.route('/recv/<ctype>', methods=['GET'])
@auth.login_required
def recv_get(ctype):
    if ctype not in ConfigKey.keys:
        return error(msg='ctype in url is error!')
    redis_key = getattr(ConfigKey, ctype)

    result = REDIS_MODEL.list_all_receivers(redis_key=redis_key)
    return jsonify(result)


# 添加一个接受人
@app.route('/recv/<ctype>', methods=['POST'])
@auth.login_required
def recv_post(ctype):
    if ctype not in ConfigKey.keys:
        return error(msg='ctype in url is error!')
    redis_key = getattr(ConfigKey, ctype)
    account = request.form.get('account', None)
    if not account:
        return error(msg='account is none')
    account = account.strip()
    result = REDIS_MODEL.add_receiver(account=account, redis_key=redis_key)
    return ok(msg=result)


# 更新一个接受人
@app.route('/recv/<ctype>', methods=['PUT'])
@auth.login_required
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

    account = account.strip()
    REDIS_MODEL.update_receiver(
        account=account, is_recv=is_recv, redis_key=redis_key)
    return ok()


# 删除一个接受人
@app.route('/recv/<ctype>', methods=['DELETE'])
@auth.login_required
def recv_del(ctype):
    if ctype not in ConfigKey.keys:
        return error(msg='ctype in url is error!')
    redis_key = getattr(ConfigKey, ctype)

    account = request.args.get('account', None)
    if not account:
        return error(msg='account is none')
    account = account.strip()
    REDIS_MODEL.delete_receiver(account=account, redis_key=redis_key)
    return ok()


# 发送消息
@app.route('/notice', methods=['POST'])
# @auth.login_required
def notice():
    title = request.form.get('title', None)
    way = request.form.get('way', None)
    content = request.form.get('content', None)
    key = request.form.get('key', None)

    if not all([title, way, content]):
        return error(msg='title or way or content is none')

    if not REDIS_MODEL.vaild_sec_key(key):
        return error(msg='key invaild!')

    if way not in ALL_SENDERS:
        return error(msg='way invaild!')

    app.logger.info('title, way, content, key :::: %s %s %s %s' %
                    (title, way, content, key))
    send_notice(way, title, content)
    return ok()


# 发送测试消息
@app.route('/notice/test/<ctype>', methods=['GET'])
@auth.login_required
def notice_test(ctype):
    test_map = {
        'mail': 'SinaEmail',
        'serverchan': 'ServerChan',
    }

    way = test_map.get(ctype, None)
    title = 'test title'
    content = 'test content'

    result = REDIS_MODEL.can_send_test_msg()
    if result is not True:
        return error(msg=f'next send time: {result}')

    app.logger.info('test send ::: title, way, content :::: %s %s %s' % (
        title, way, content))
    send_notice(way, title, content)
    return ok()


def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=Config.API_SERVER_PORT)


if __name__ == '__main__':
    run()
