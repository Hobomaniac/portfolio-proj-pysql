from flask import Blueprint, jsonify, abort, request 
from ..models import Route, db, Label

bp = Blueprint('routes', __name__, url_prefix='/routes')

@bp.route('', methods=['GET'])
def index():
    routes = Route.query.all()
    result = []
    for r in routes:
        result.append(r.serialize())
    return jsonify(result)

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    r = Route.query.get_or_404(id, "Route not found")
    return jsonify(r.serialize())

#TODO: Add some checks
@bp.route('', methods=['POST'])
def create():

    if 'name' not in request.json or 'date' not in request.json or 'user_id' not in request.json:
        return abort(400)
    
    _location = None 
    _distance = None 
    _time_length = None 
    if 'location' in request.json:
        _location = request.json['location']
    if 'distance' in request.json:
        _distance = request.json['distance']
    if 'time_length' in request.json:
        _time_length = request.json['time_length']

    r = Route(
        name=request.json['name'],
        date=request.json['date'],
        location=_location,
        distance=_distance,
        time_length=_time_length,
        user_id=request.json['user_id']
    )

    db.session.add(r)
    db.session.commit()
    return jsonify(r.serialize())

@bp.route('/<int:id>', methods=['DELETE'])
def delete(id: int):
    r = Route.query.get_or_404(id, "Route not found")
    try:
        db.session.delete(r)
        db.session.commit()
        return jsonify(True)
    except:
        return jsonify(False)
    
#TODO: add date casting and some checks
@bp.route('/<int:id>', methods=['PATCH'])
def update(id: int):
    r = Route.query.get_or_404(id)

    if 'name' in request.json:
        r.name = request.json['name']

    if 'date' in request.json:
        r.date = request.json['date']

    if 'location' in request.json:
        r.location = request.json['location']

    if 'distance' in request.json:
        r.distance = request.json['distance']

    if 'time_length' in request.json:
        r.time_length = request.json['time_length']

    try:
        db.session.commit()
        return jsonify(r.serialize())
    except:
        return jsonify(False)
    
@bp.route('/<int:id>/labels', methods=['POST'])
def add_labels_to_route(id):
    r = Route.query.get_or_404(id)

    if 'label_ids' not in request.json:
        return abort(400, "No valid labels provided")
    
    labels = Label.query.filter(Label.id.in_(request.json['label_ids'])).all()

    r.labels.extend(labels)
    db.session.commit()
    return jsonify(True)

@bp.route('/<int:id>/labels', methods=['GET'])
def get_labels_for_route(id: int):
    r = Route.query.get_or_404(id)

    result = []
    for l in r.labels:
        result.append(l.serialize())
    return jsonify(result)

@bp.route('/<int:id>/labels', methods=['DELETE'])
def delete_labels_from_route(id: int):
    r = Route.query.get_or_404(id)

    if 'label_ids' not in request.json:
        return abort(400, "No valid labels provided")
    
    labels = Label.query.filter(Label.id.in_(request.json['label_ids'])).all()

    try:
        for l in labels:
            r.labels.remove(l)

        db.session.commit()
        return jsonify(True)
    except:
        return jsonify({
            "error": "Did not remove label(s)"
        })