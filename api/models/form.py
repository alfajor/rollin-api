from pydantic import BaseModel

class FormData(BaseModel):
    email: str