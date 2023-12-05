from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


class HeroTeamLink(SQLModel, table=True):
    team_id: Optional[int] = Field(
        default=None, foreign_key="team.id", primary_key=True
    )
    hero_id: Optional[int] = Field(
        default=None, foreign_key="hero.id", primary_key=True
    )


# ==================== Team ====================

class TeamBase(SQLModel):
    name: str = Field(index=True)
    headquarters: str


class TeamCreate(TeamBase):
    pass


class TeamPatch(SQLModel):
    name: Optional[str] = None
    headquarters: Optional[str] = None


class Team(TeamBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    heroes: list["Hero"] = Relationship(back_populates="teams", link_model=HeroTeamLink)


class TeamRead(TeamBase):
    id: int


# ==================== Hero ====================

class HeroBase(SQLModel):
    name: str = Field(index=True)
    secret_name: str
    age: Optional[int] = Field(default=None, index=True)


class HeroCreate(HeroBase):
    pass


class HeroPatch(SQLModel):
    name: Optional[str] = None
    secret_name: Optional[str] = None
    age: Optional[int] = None


class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    teams: list[Team] = Relationship(back_populates="heroes", link_model=HeroTeamLink)


class HeroRead(HeroBase):
    id: int


class HeroReadWithTeams(HeroRead):
    teams: list[TeamRead] = []


class TeamReadWithHeroes(TeamRead):
    heroes: list["HeroRead"] = []