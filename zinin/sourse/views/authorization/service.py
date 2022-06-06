# from flask import Blueprint, render_template, abort, jsonify
# from flask import Flask, render_template, request, redirect, make_response
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

from functools import wraps


from settings import *
from log import logger


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})
        try:
            data = jwt.decode(token, SECRET_KEY)
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args, **kwargs)
    return decorator


def is_kto_to(adm):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                result = request.json
                username = result["username"]
                res = db_mongo.check_users(username)
                if res:
                    if adm >= int(res["admin"]):
                        return f(*args, **kwargs)
                return jsonify({'message': 'No access'})
            except:
                return jsonify({'message': 'No access'})

        return wrapper
    return decorator

def login_inside(result):
    if "username" in result and "password" in result:
        username = result["username"]
        password = str(result["password"])
        res = db_mongo.check_users(username)
        if res:
            if check_password_hash(res['password'], password):
                token = jwt.encode(
                    {'public_id': res['user_id'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                    SECRET_KEY)
                return {'token': token}
        return {'message': 'could not verify'}  # make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})

def register_inside(result):
    if "username" in result and "password" in result:
        username = result["username"]
        password = str(result["password"])
        adm = 0
        if username == "admin":
            adm = 1
        hashed_password = generate_password_hash(password, method='sha256')
        res = db_mongo.insert_users(str(username), str(hashed_password), adm)
        logger.error(res)
        if res:
            return {'message': 'registered successfully'}
    return {'message': 'could not register'}  # make_response('could not register',  401, {'WWW.Authentication': 'Basic realm: "registration is not successful"'})
