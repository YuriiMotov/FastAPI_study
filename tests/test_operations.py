from httpx import AsyncClient

async def test_add_specific_operation(ac: AsyncClient):
    response = await ac.post(
        '/operations/',
        json={
            "quantity": "string",
            "figi": "",
            "instrument_type": "BTC",
            "date": "2023-10-24T15:41:48.071Z",
            "type": "sell"
        }
    )
    assert response.status_code == 201
    json_res = response.json()
    assert json_res["id"] == 1
    assert json_res["type"] == "sell"
    assert json_res["instrument_type"] == "BTC"


async def test_get_specific_operations(ac: AsyncClient):
    response = await ac.get(
        '/operations/?operation_type=sell'
    )
    assert response.status_code == 200
    json_res = response.json()
    assert len(json_res) == 1
    assert json_res[0]["id"] == 1
    assert json_res[0]["type"] == "sell"
    assert json_res[0]["instrument_type"] == "BTC"

