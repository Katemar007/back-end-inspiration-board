from flask import request, abort, make_response, Response
from ..db import db
import os
import requests

def validate_model(cls, id):
    try: 
        id = int(id)
    except: 
        abort(make_response({"details": "Invalid data"}, 400))
    
    query = db.select(cls).where(cls.card_id == id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"details": "Not found"}, 404))
    return model


def create_model(cls, model_data):
    try: 
        new_model = cls.from_dict(model_data)

    except KeyError as e:
        response = {"message": f"Invalid request: missing {e.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()
    return new_model.to_dict(), 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute): 
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]

    return models_response

# additional feature: every time a new card is made, 
# it sends a message to the team's public Slack channel

def send_message_card_created_slack(card_message):
    slack_url = os.environ.get("SLACK_BOT_PATH")
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_TEST_CHANNEL_ID")

    message = {
        "channel": slack_channel,
        "text": f"Someone just created a card {card_message}"
    }

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(slack_url, json=message, headers=headers)

    if not response.ok:
        try:
            error_info = response.json()
        except ValueError:
            error_info = response.text

        response_data = {
            "message": "Slack message failed",
            "status_code": response.status_code,
            "slack_error": error_info
        }
        abort(make_response(response_data, 500))