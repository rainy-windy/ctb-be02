from pydantic import BaseModel, Extra


class Message(BaseModel):
    content: str
    id: str
    role: str
    