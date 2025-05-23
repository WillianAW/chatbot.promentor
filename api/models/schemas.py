from pydantic import BaseModel, Field

class ItemBase(BaseModel):
    name: str = Field(..., example="Celular")
    description: str | None = Field(None, example="Smartphone último modelo")

class ItemCreate(ItemBase):
    price: float = Field(..., gt=0, example=1999.90)

class Item(ItemBase):
    id: int
    price: float
    
    class Config:
        orm_mode = True