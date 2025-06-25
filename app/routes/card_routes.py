from flask import Blueprint, request, Response
from flask import request, abort, make_response
from ..models.card import Card
from .card_utilities import validate_model
from ..db import db
from sqlalchemy import asc, desc
import requests
import os
from dotenv import load_dotenv
load_dotenv()

bp = Blueprint("cards_bp", __name__, url_prefix = "/cards")

@bp.post("")
def create_new_card():
    request_body = request.get_json()
    if (
        not request_body
        or "message" not in request_body
    ):
        abort(make_response({"details": "Invalid data"}, 400))
    new_card = Card.from_dict(request_body)
    db.session.add(new_card)
    db.session.commit()

    return {
            "card":{
            "card_id" : new_card.card_id,
            "message": new_card.message,
            "likes_count": new_card.likes_count
            }
        }, 201

@bp.get("")
def get_all_cards():
    query = db.select(Card)
    sort_param = request.args.get("sort")

    if sort_param == "asc":
        query = db.select(Card).order_by(desc(Card.card_id))
    else:
        query = db.select(Card).order_by(asc(Card.card_id))
    
    cards = db.session.scalars(query)
    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())

    return cards_response

@bp.get("/<card_id>")

def get_one_card(card_id):
    card = validate_model(Card, card_id)
    
    response = {        
            "card_id" : card.card_id,
            "message": card.message,
            "likes_count": card.likes_count
        }
    if card.board_id is not None:
        response["board_id"] = card.board_id
    return {"card": response}

@bp.put("/<card_id>")
def update_card(card_id):
    card = validate_model(Card, card_id)

    request_body = request.get_json()

    card.message = request_body["message"]
    card.likes_count = request_body["likes_count"]
 
    db.session.commit()

    return Response(status = 204, mimetype = "application/json")

# @bp.patch("/<id>/_")
# def change_card(card_id):
#     card = validate_model(Card, card_id)

#     db.session.commit()
#     return "", 204

@bp.delete("/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return Response(status = 204, mimetype = "application/json")