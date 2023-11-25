import random

from starlette.testclient import WebSocketTestSession

from tests.e2e.conftest import client


def test_send_msg():
    CLIENT_ID = random.randint(1000, 2000)
    TEXT = "Hello, World!"

    websocket: WebSocketTestSession
    with client.websocket_connect(f'/chat/ws/{CLIENT_ID}') as websocket:
        websocket.send_text(TEXT)
        data = websocket.receive_text()
        assert data == f"#{CLIENT_ID} says: {TEXT}"


def test_send_msg_two_clients():
    CLIENT1_ID = random.randint(1000, 2000)
    CLIENT2_ID = random.randint(1000, 2000)
    TEXT = "Hello, World!"

    websocket1: WebSocketTestSession
    websocket2: WebSocketTestSession
    with client.websocket_connect(f'/chat/ws/{CLIENT1_ID}') as websocket1:
        with client.websocket_connect(f'/chat/ws/{CLIENT2_ID}') as websocket2:
            websocket1.send_text(TEXT)
            data = websocket1.receive_text()
            assert data == f"#{CLIENT1_ID} says: {TEXT}"
            data = websocket2.receive_text()
            assert data == f"#{CLIENT1_ID} says: {TEXT}"

