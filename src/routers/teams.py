from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database import get_async_session, AsyncSession
from models.heroes_teams import TeamCreate, Team, TeamRead, TeamReadWithHeroes, TeamPatch


teams_router = APIRouter(
    prefix="/teams",
    tags=["heroes_teams"]
)


@teams_router.get("/", response_model=list[TeamReadWithHeroes])
async def get_teams(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    offset: int = 0,
    limit: int = 10
):
    st = select(Team).options(selectinload(Team.heroes)).limit(limit).offset(offset)
    teams = (await session.scalars(st)).all()
    return teams


@teams_router.get(
    "/{team_id}", response_model=TeamReadWithHeroes,
    responses={
        404: {"description": "Team not found"}
    }
)
async def get_team(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    team_id: int   
):
    team = await session.get(Team, team_id, options=[selectinload(Team.heroes)])
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id={team_id} doesn't exist"
        )
    return team


@teams_router.post("/", response_model=TeamRead, status_code=201)
async def add_team(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    team_data: TeamCreate
):
    team = Team(**team_data.model_dump())
    session.add(team)
    await session.commit()
    await session.refresh(team)
    return team


@teams_router.patch(
    "/{team_id}",
    response_model=TeamRead,
    responses={
        404: {"description": "Team not found"}
    }
)
async def edit_team(
    session: Annotated[AsyncSession, Depends(get_async_session)],
    team_id: int,
    team_data: TeamPatch
):
    team = await session.get(Team, team_id)
    if team is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Team with id={team_id} doesn't exist"
        )
    for k, v in team_data.model_dump(exclude_unset=True).items():
        setattr(team, k, v)
    await session.commit()
    return team

