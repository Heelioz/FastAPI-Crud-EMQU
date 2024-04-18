from pydantic import BaseModel

class PC(BaseModel):
    id: str | None = None  
    name: str
    ip: str
    ping: bool
    count: int