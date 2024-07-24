from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()
# get: lấy dữ liệu từ máy chủ
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
# post: gửi dữ liệu tới máy chủ
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/")
def create_item(item: Item):
    return {"item": item}
# put: sử dụng để cập nhật toàn bộ tài nguyên trên máy chủ
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_id": item_id, "item": item}

# delete: xóa 1 tài nguyên trên máy chủ
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"item_id": item_id, "message": "Item deleted"}
