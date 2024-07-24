from fastapi import FastAPI

# Khởi tạo FastAPI
app = FastAPI()

# Định nghĩa một endpoint đơn giản
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Định nghĩa một endpoint với parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
