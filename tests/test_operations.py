import asyncio
from httpx import AsyncClient
import pytest


@pytest.mark.asyncio_cooperative
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
    await asyncio.sleep(1)
    assert response.status_code == 201
    json_res = response.json()
    assert json_res["type"] == "sell"
    assert json_res["instrument_type"] == "BTC"


@pytest.mark.asyncio_cooperative
async def test_add_specific_operation2(ac: AsyncClient):
    response = await ac.post(
        '/operations/',
        json={
            "quantity": "string",
            "figi": "",
            "instrument_type": "USD",
            "date": "2023-10-24T15:41:48.071Z",
            "type": "buy"
        }
    )
    await asyncio.sleep(1)
    assert response.status_code == 201
    json_res = response.json()
    assert json_res["type"] == "buy"
    assert json_res["instrument_type"] == "USD"


@pytest.mark.asyncio_cooperative
async def test_add_specific_operation3(ac: AsyncClient):
    response = await ac.post(
        '/operations/',
        json={
            "quantity": "string",
            "figi": "",
            "instrument_type": "EUR",
            "date": "2023-10-24T15:41:48.071Z",
            "type": "buy"
        }
    )
    await asyncio.sleep(1)
    assert response.status_code == 201
    json_res = response.json()
    assert json_res["type"] == "buy"
    assert json_res["instrument_type"] == "EUR"


@pytest.mark.asyncio_cooperative
async def test_add_specific_operation4(ac: AsyncClient):
    response = await ac.post(
        '/operations/',
        json={
            "quantity": "string",
            "figi": "",
            "instrument_type": "SAT",
            "date": "2023-10-24T15:41:48.071Z",
            "type": "sell"
        }
    )
    await asyncio.sleep(1)
    assert response.status_code == 201
    json_res = response.json()
    assert json_res["type"] == "sell"
    assert json_res["instrument_type"] == "SAT"


@pytest.mark.asyncio_cooperative
async def test_add_specific_operation5(ac: AsyncClient):
    response = await ac.post(
        '/operations/',
        json={
            "quantity": "string",
            "figi": "",
            "instrument_type": "USD",
            "date": "2023-10-24T15:41:48.071Z",
            "type": "sell"
        }
    )
    await asyncio.sleep(1)
    assert response.status_code == 201
    json_res = response.json()
    assert json_res["type"] == "sell"
    assert json_res["instrument_type"] == "USD"


