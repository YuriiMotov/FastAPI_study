from  asyncio import sleep as asleep
import random

from fastapi import HTTPException
import pytest

from token_service import TokenService, MemoryStorage, InvalidToken

@pytest.mark.asyncio_cooperative
async def test_refresh_token_invalidate():
    token_service = TokenService(
        secret="123", storage_class=MemoryStorage, storage_config={},
        access_token_expire_minutes=1, refresh_token_expire_minutes=1
    )

    token_data = {"sub": "username", "scopes": ["me"]}

    # Create first token
    token1 = await token_service.create_refresh_token(token_data)

    # Validate first token and create second
    token1_decoded = await token_service.validate_refresh_token(token1, HTTPException)
    token2 = await token_service.create_refresh_token(token_data)
    # ... First token is invalid now

    await asleep(1) # Diff. between tokens issue datetime should be at least 1 sec.

    # Validate second token and create third
    token2_decoded = await token_service.validate_refresh_token(token2, HTTPException)
    token3 = await token_service.create_refresh_token(token_data)
    # ... Second token is invalid now

    await asleep(1) # We can't invalidate token during first second after it's issue

    # Try validating second token again. It will raise InvalidToken exception
    with pytest.raises(InvalidToken):
        token2_decoded = await token_service.validate_refresh_token(token2, HTTPException)
        # ... All tokens of this user are invalid now
    
    # Try validating third token. It will raise InvalidToken exception
    with pytest.raises(InvalidToken):
        token3_decoded = await token_service.validate_refresh_token(token3, HTTPException)


