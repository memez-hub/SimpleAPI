from pydantic import BaseModel

class AmenityResponce(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True