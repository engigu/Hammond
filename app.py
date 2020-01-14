import datetime
import json
from flask import Flask, render_template, jsonify, request
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_httpauth import HTTPBasicAuthreid

from core.db import CookiesPoolRedis
from config import Config

REDIS_MODEL = CookiesPoolRedis(uri=Config.REDIS_URI)
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
@app.route('/cookies_all', methods=['GET'])
# @auth.login_required
def cookies_all():
    page = request.args.get('page')
    size = request.args.get('size')
    cookies, total = REDIS_MODEL.query_all_cookies(page=page, size=size)
    return jsonify({"total": total, "cookies":  cookies})


def run():
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=True, host='0.0.0.0', port=Config.API_SERVER_PORT)


if __name__ == '__main__':
    run()
