from flask import abort, make_response, Response
from ..db import db
import os
import requests


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f":{cls.__name__} with {model_id} invalid"}
        abort(make_response(response, 400))
    
    query = db.select(cls).where(cls.board_id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} with {model_id} does not exist"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        response = {"details": "Invalid data"}
        # response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
        
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

def delete_model(cls, model_id):
    model = validate_model(cls, model_id)

    db.session.delete(model)
    db.session.commit()

    return Response(status=204, mimetype="application/json")


def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute): 
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    models = db.session.scalars(query.order_by(cls.board_id))
    models_response = [model.to_dict() for model in models]

    return models_response