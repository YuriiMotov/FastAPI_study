from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_async_session, AsyncSession
from models.heroes_teams import (
    HeroCreate, Hero, HeroRead, HeroReadWithTeams, HeroPatch,
    Team, TeamRead
) 


heroes_router = APIRouter(
    prefix="/heroes",
    tags=["heroes_teams"]
)


@heroes_router.get("/", response_model=list[HeroReadWithTeams])
async def get_heroes(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    offset: int = 0,
    limit: int = 10
):
    st = select(Hero).options(selectinload(Hero.teams)).limit(limit).offset(offset)
    heroes = (await session.scalars(st)).all()
    return heroes


@heroes_router.get(
    "/{hero_id}",
    response_model=HeroReadWithTeams,
    responses={
        404: {"description": "Hero not found"}
    }
)
async def get_hero(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hero_id: int   
):
    hero = await session.get(Hero, hero_id, options=[selectinload(Hero.teams)])
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id={hero_id} doesn't exist"
        )
    return hero


@heroes_router.post("/", response_model=HeroRead, status_code=201)
async def add_hero(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hero_data: HeroCreate
):
    hero = Hero(**hero_data.model_dump())
    session.add(hero)
    await session.commit()
    await session.refresh(hero)
    return hero


@heroes_router.patch(
    "/{hero_id}",
    response_model=HeroRead,
    responses={
        404: {"description": "Hero not found"}
    }
)
async def edit_hero(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hero_id: int,
    hero_data: HeroPatch
):
    hero = await session.get(Hero, hero_id)
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id={hero_id} doesn't exist"
        )
    for k, v in hero_data.model_dump(exclude_unset=True).items():
        setattr(hero, k, v)
    await session.commit()
    return hero


@heroes_router.get(
    "/{hero_id}/teams",
    response_model=list[TeamRead],
    responses={
        404: {"description": "Hero not found"}
    }
)
async def get_teams_of_hero(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hero_id: int
):
    hero = await session.get(Hero, hero_id, options=[selectinload(Hero.teams)])
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id={hero_id} doesn't exist"
        )
    return hero.teams


@heroes_router.post(
    "/{hero_id}/teams", response_model=list[TeamRead],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Hero not found"}
    }
)
async def add_hero_to_team(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hero_id: int,
    team_id: Annotated[int, Body()]
):
    team = await session.get(Team, team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team with id={team_id} doesn't exist"
        )
    hero = await session.get(Hero, hero_id, options=[selectinload(Hero.teams)])
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id={hero_id} doesn't exist"
        )
    if team not in hero.teams:
        hero.teams.append(team)
    await session.commit()
    await session.refresh(hero)
    return hero.teams


@heroes_router.delete(
    "/{hero_id}/teams",
    response_model=list[TeamRead],
    responses={
        400: {"description": "Bad request"},
        404: {"description": "Hero not found"}
    }
)
async def remove_hero_from_team(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    hero_id: int,
    team_id: Annotated[int, Body()]
):
    team = await session.get(Team, team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Team with id={team_id} doesn't exist"
        )
    hero = await session.get(Hero, hero_id, options=[selectinload(Hero.teams)])
    if hero is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Hero with id={hero_id} doesn't exist"
        )
    if team in hero.teams:
        hero.teams.remove(team)
    await session.commit()
    await session.refresh(hero)
    return hero.teams
