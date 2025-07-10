from flask import Blueprint, abort, make_response, request, Response
from app.models.board import Board
from app.models.card import Card
from ..db import db
from .board_utilities import validate_model_b, create_model, delete_model, get_models_with_filters
import requests
import os

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")


@bp.post("")
def create_board():
    request_body = request.get_json()
    new_board, status_code = create_model(Board, request_body)

    return {"board": new_board}, status_code


@bp.get("")
def get_all_boards():
    filters = {}

    title_param = request.args.get("title")
    if title_param:
        filters["title"] = title_param

    if filters:
        return get_models_with_filters(Board, filters)
    
    else:
        query = db.select(Board).order_by(Board.board_id)
        boards = db.session.scalars(query)
        return [board.to_dict() for board in boards]


@bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_model_b(Board, board_id)
    return {"board": board.to_dict()}


@bp.put("/<board_id>")
def update_one_board(board_id):
    board = validate_model_b(Board, board_id)
    request_body = request.get_json()

    board.title = request_body["title"]
    board.owner = request_body["owner"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@bp.delete("/<board_id>")
def delete_one_board(board_id):

    return delete_model(Board, board_id)


