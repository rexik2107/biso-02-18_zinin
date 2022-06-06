# from flask import Blueprint, render_template, abort, jsonify
# from flask import Flask, render_template, request, redirect, make_response
from functools import wraps
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from aiohttp import web
# from flask_cors import CORS, cross_origin

from settings import *
from .service import login_inside, register_inside

from commands import Command
from log import logger

cmd = Command()

#authorization_all = Blueprint('authorization_all', __name__)

# @authorization_all.after_request # blueprint can also be app~~
# def after_request(response):
#     header = response.headers
#     header['Access-Control-Allow-Origin'] = 'http://localhost'
#     header['Access-Control-Allow-Credentials'] = True
#     return response


@cmd('/login', methods=["POST", "OPTIONS"])
#@cross_origin()
async def login(request: web.Request, data: dict):
    db_mongo.insert_users("admin", generate_password_hash("rolgroup228", method='sha256'), 1)  # TODO: костыль для создания админки
    #db_mongo.insert_users("admin", generate_password_hash("rolgroup228", method='sha256'), 0)  # TODO: костыль для создания обычного юзера
    #result = request.json
    return login_inside(data)
    # if "username" in result and "password" in result:
    #     username = result["username"]
    #     password = str(result["password"])
    #     res = db.check_users(username)
    #     if res:
    #         if check_password_hash(res[1], password):
    #             token = jwt.encode(
    #                 {'public_id': res[0], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
    #                 SECRET_KEY)
    #             return jsonify({'token': token})
    #     return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

@cmd('/register', methods=["POST", "OPTIONS"])
async def register(request: web.Request, data: dict):
    db.insert_users("admin", generate_password_hash("rolgroup228", method='sha256'), 1)  # TODO: костыль для создания админки
    #db.insert_users("admin", generate_password_hash("rolgroup228", method='sha256'), 0)  # TODO: костыль для создания обычного юзера
    #result = request.json
    #print(result)
    return register_inside(data)
    # if "username" in result and "password" in result:
    #     username = result["username"]
    #     password = str(result["password"])
    #     adm = 0
    #     if username == "admin":
    #         adm = 1
    #     hashed_password = generate_password_hash(password, method='sha256')
    #     res = db.insert_users(str(username), str(hashed_password), adm)
    #     if res:
    #         return jsonify({'message': 'registered successfully'})
    # return make_response('could not register',  401, {'WWW.Authentication': 'Basic realm: "registration is not successful"'})
