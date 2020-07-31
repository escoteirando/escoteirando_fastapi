from typing import Optional

from pydantic import BaseModel

from src.app import app


class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.put("/api/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
