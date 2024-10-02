from pydantic import BaseModel

class UserData(BaseModel):
    id: int
    email: str
    apiKey: str
    userToken: str