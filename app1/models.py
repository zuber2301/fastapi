from pydantic import BaseModel
class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    is_offer: bool = None