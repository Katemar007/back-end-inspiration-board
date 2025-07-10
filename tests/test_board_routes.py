from app.models.board import Board
from app import db

def test_create_board(client):
    response = client.post("/boards", json={
        "title": "Travel",
        "owner": "Mr.Sloth"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["board"]["title"] == "Travel"
    assert data["board"]["owner"] == "Mr.Sloth"

def test_get_all_boards(client):
    db.session.add(Board(title="Board A", owner="Owner A"))
    db.session.add(Board(title="Board B", owner="Owner B"))
    db.session.commit()

    response = client.get("/boards")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["title"] == "Board A"

def test_get_one_board(client):
    board = Board(title="One lonely board", owner="Someone")
    db.session.add(board)
    db.session.commit()

    response = client.get(f"/boards/{board.board_id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["board"]["owner"] == "Someone"

def test_update_board(client):
    board = Board(title="Wake up!", owner="Me")
    db.session.add(board)
    db.session.commit()

    response = client.put(f"/boards/{board.board_id}", json={
        "title": "Sleep!",
        "owner": "You"
    })
    assert response.status_code == 204

    updated = Board.query.get(board.board_id)
    assert updated.title == "Sleep!"
    assert updated.owner == "You"

def test_delete_board(client):
    board = Board(title="Destroy me!", owner="Board destroyer")
    db.session.add(board)
    db.session.commit()

    response = client.delete(f"/boards/{board.board_id}")
    assert response.status_code == 204

    deleted = Board.query.get(board.board_id)
    assert deleted is None

def test_create_card_with_invalid_board_id(client):
    response = client.post("/boards/999/cards", json={"message": "No board ID"})

    # Assert that the response is a 404 Not Found
    assert response.status_code == 404
    response_data = response.get_json()

    assert "message" in response_data
    assert "Board 999 does not exist" in response_data["message"]

def test_create_board_missing_title(client):
    response = client.post("/boards", json={"owner": "Tester"})
    
    assert response.status_code == 400
    assert response.get_json() == {"details": "Invalid data"}