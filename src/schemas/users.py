from pydantic import BaseModel, ConfigDict


class UserSchemaBase(BaseModel):
    name: str

class UserSchema(UserSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class UserSchemaAdd(UserSchemaBase):
    pass

    