from flask import Blueprint, request, Response
from flask import abort, make_response
from ..models.card import Card
from ..models.board import Board
from .card_utilities import validate_model, send_message_card_created_slack
from ..db import db
import requests
import os
from dotenv import load_dotenv
load_dotenv()

bp = Blueprint("cards_bp", __name__)

@bp.post("/boards/<board_id>/cards")
def create_new_card(board_id):
    request_body = request.get_json()
    if (
        not request_body
        or "message" not in request_body
    ):
        abort(make_response({"details": "Invalid data"}, 400))
    request_body["board_id"] = int(board_id)
    new_card = Card.from_dict(request_body)
    db.session.add(new_card)
    db.session.commit()

    send_message_card_created_slack(new_card.message)

    return {
            "card":new_card.to_dict()
        }, 201

@bp.get("/boards/<board_id>/cards")
def get_all_cards_by_board(board_id):
    query = db.select(Card).filter_by(board_id = board_id)
    cards = db.session.scalars(query)
    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())

    return cards_response

@bp.put("/boards/<board_id>/cards/<card_id>/like")
def like_card(board_id, card_id):
    card = validate_model(Card, card_id)
    card.likes_count += 1
    db.session.commit()

    return {"card": card.to_dict()}

@bp.delete("/cards/<card_id>")
def delete_card(card_id):
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return Response(status = 204, mimetype = "application/json")

# @bp.put("/cards/<card_id>/like")
# def like_card(card_id):
#     card = validate_model(Card, card_id)
#     card.likes_count += 1
#     db.session.commit()

#     return {"card": card.to_dict()}
