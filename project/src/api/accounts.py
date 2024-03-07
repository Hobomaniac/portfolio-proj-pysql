from flask import Blueprint, jsonify, abort, request 
from ..models import Account, db

import hashlib 
import secrets 
def scramble(password: str): 
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('accounts', __name__, url_prefix='/accounts')

@bp.route('', methods=['GET'])
def index():
    accounts = Account.query.all()
    result = []
    for a in accounts:
        result.append(a.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    a = Account.query.get_or_404(id, 'Account not found')
    return jsonify(a.serialize())

@bp.route('', methods=['POST'])
def create():

    attr_check = [
        'email',
        'password',
        'user_id'
    ]

    for attr in attr_check:
        if attr not in request.json:
            return abort(400, attr + " not in request.json")
    
    if len(request.json['password']) < 8:
        return abort(400, "Password needs 8 characters.")
    
    _username = None 
    if 'username' in request.json and len(request.json['username']) > 1:
        _username = request.json['username']
    
    a = Account(
        username=_username,
        password=scramble(request.json['password']),
        email=request.json['email'],
        user_id=request.json['user_id']
    )

    db.session.add(a)
    db.session.commit()
    return jsonify(a.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    a = Account.query.get_or_404(id, 'Account not found')
    try:
        db.session.delete(a)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    a = Account.query.get_or_404(id)

    if 'username' in request.json: 
        if len(request.json['username']) > 2:
            a.username = request.json['username']
        else:
            return abort(400, "Username needs 2 or more characters")
        
    if 'password' in request.json:
        if len(request.json['password']) >= 8:
            a.password = scramble(request.json['password'])
        else:
            return abort(400, "Password needs to 8 or more characters")
        
    if 'email' in request.json:
        a.email = request.json['email']

    try:
        db.session.commit()
        return jsonify(a.serialize())
    except:
        return jsonify(False)
