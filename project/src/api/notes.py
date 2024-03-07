from flask import Blueprint, jsonify, abort, request 
from ..models import Note, db 

bp = Blueprint('notes', __name__, url_prefix='/notes')

@bp.route('', methods=['GET'])
def index():
    notes = Note.query.all()
    result = []
    for n in notes:
        result.append(n.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    n = Note.query.get_or_404(id)
    return jsonify(n.serialize())

@bp.route('', methods=['POST'])
def create():

    attr_check = [
        'title',
        'time_stamp',
        'route_id'
    ]

    for attr in attr_check:
        if attr not in request.json:
            abort(400)

    if len(request.json['title']) < 1:
        abort(400)

    _description = None 
    if 'description' in request.json:
        _description = request.json['description']

    n = Note(
        title=request.json['title'],
        description=_description,
        time_stamp=request.json['time_stamp'],
        route_id=request.json['route_id']
    )

    try:
        db.session.add(n)
        db.session.commit(n)
        return jsonify(n.serialize())
    except:
        return jsonify(False)
    pass 

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    n = Note.query.get_or_404(id)
    try:
        db.session.delete(n)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
    
@bp.route('/<int:id>', methods=['PATCH'])
def update(id: int):
    n = Note.query.get_or_404(id)

    if 'title' in request.json:
        if len(request.json['title']) >= 1:
            n.title = request.json['title']
        else:
            return abort(400)
        
    if 'description' in request.json:
        n.description = request.json['description']

    if 'time_stamp' in request.json:
        n.time_stamp = request.json['time_stamp']

    try:
        db.session.commit()
        return jsonify(n.serialize())
    except:
        return jsonify(False)
    pass