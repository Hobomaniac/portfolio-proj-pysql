from flask import Blueprint, jsonify, abort, request 
from ..models import User, db
from datetime import datetime

bp = Blueprint('users', __name__, url_prefix='/users')

"""
Methods:
    index
    show
    create
    delete
    update
"""

@bp.route('', methods=['GET'])
def index():
    users = User.query.all()
    result = []
    for u in users:
        result.append(u.serialize())
    return jsonify(result)


@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id, "User not found")
    return jsonify(u.serialize())


@bp.route('', methods=['POST'])
def create():
    if 'first_name' not in request.json or 'last_name' not in request.json:
        return abort(400)
    
    if len(request.json['first_name']) < 1 or len(request.json['last_name']) < 1:
        return abort(400)

    _birthdate = None
    if 'birthdate' in request.json:
        try:
            _birthdate = datetime.strptime(request.json['birthdate'], '%Y-%m-%d')
        except ValueError:
            # If parsing fails, the format is incorrect
            return abort(400, "Invalid 'birthdate' format. Use YYYY-MM-DD.")
    
    u = User(
        first_name = request.json['first_name'],
        last_name = request.json['last_name'],
        birthdate = _birthdate
    )

    db.session.add(u)
    db.session.commit()
    return jsonify(u.serialize())


@bp.route('/<int:id>', methods=['DELETE'])
def delete(id:int):
    u = User.query.get_or_404(id, "User not found")
    try:
        db.session.delete(u)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
    
    
@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    u = User.query.get_or_404(id)

    attr_check = [
        'first_name',
        'last_name',
        'birthdate'
    ]

    flag = False
    for attr in attr_check:
        if attr in request.json:
            flag = True
            break

    if not flag:
        return abort(400)

    if 'first_name' in request.json:
        if len(request.json['first_name']) > 1:
            u.first_name = request.json['first_name']
        else:
            return abort(400)
        
    if 'last_name' in request.json:
        if len(request.json['last_name']) > 1:
            u.last_name = request.json['last_name']
        else:
            return abort(400)
        
    
    if 'birthdate' in request.json:
        try:
            birthdate = datetime.strptime(request.json['birthdate'], '%Y-%m-%d')
            # If parsing succeeds, assign the date to the user object or use it as needed
            u.birthdate = birthdate#.strftime('%Y-%m-%d')  # Optional: Convert it back to string for consistency
        except ValueError:
            # If parsing fails, the format is incorrect
            return abort(400, "Invalid 'birthdate' format. Use YYYY-MM-DD.")
        
    try:
        db.session.commit()
        return jsonify(u.serialize())
    except:
        return jsonify(False)