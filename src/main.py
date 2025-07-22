from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI(title="Sample FastAPI App", version="1.0.0")

# Pydantic models for request/response
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    total: float

# In-memory storage for demo
items_db = []
item_counter = 1

@app.get("/")
async def root():
    return {"message": "Hello World! Welcome to FastAPI"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/items")
async def get_items():
    return {"items": items_db}

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    global item_counter

    total = item.price
    if item.tax:
        total += item.tax

    new_item = {
        "id": item_counter,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax,
        "total": total
    }

    items_db.append(new_item)
    item_counter += 1

    return new_item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    for i, existing_item in enumerate(items_db):
        if existing_item["id"] == item_id:
            total = item.price
            if item.tax:
                total += item.tax

            updated_item = {
                "id": item_id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "tax": item.tax,
                "total": total
            }
            items_db[i] = updated_item
            return updated_item

    return {"error": "Item not found"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            deleted_item = items_db.pop(i)
            return {"message": f"Item {item_id} deleted", "deleted_item": deleted_item}

    return {"error": "Item not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
