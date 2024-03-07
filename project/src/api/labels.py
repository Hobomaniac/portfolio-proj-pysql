from flask import Blueprint, jsonify, abort, request 
from ..models import Label, db

bp = Blueprint('labels', __name__, url_prefix='/labels')

@bp.route('', methods=['GET'])
def index():
    labels = Label.query.all()
    result = []
    for l in labels:
        result.append(l.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    l = Label.query.get_or_404(id, "Label not found")
    return jsonify(l.serialize())

@bp.route('', methods=['POST'])
def create():
    if 'name' not in request.json:
        return abort(400)
    
    if len(request.json['name']) < 1:
        return abort(400, "Length of label needs at least 1 character")
    
    l = Label(
        name=request.json['name']
    )

    db.session.add(l)
    db.session.commit()
    return jsonify(l.serialize()) 

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    l = Label.query.get_or_404(id)
    try:
        db.session.delete(l)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
    
@bp.route('/<int:id>', methods=['PATCH'])
def update(id: int):
    l = Label.query.get_or_404(id)

    if "name" not in request.json:
        return abort(400)
    
    if len(request.json['name']) >= 1:
        l.name = request.json['name']
    else:
        return abort(400, "Length of label needs at least 1 character")
    
    try:
        db.session.commit()
        return jsonify(l.serialize())
    except:
        return jsonify(False)