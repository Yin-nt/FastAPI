from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
'''
- Đọc nội dung yêu cầu dưới dạng JSON.
- Chuyển đổi các loại tương ứng (nếu cần).
- Xác thực dữ liệu: nếu dữ liệu không hợp lệ, nó sẽ trả về một lỗi rõ ràng và chính xác, 
chỉ ra chính xác dữ liệu không chính xác ở đâu và dữ liệu nào.
- Cung cấp cho bạn dữ liệu nhận được trong tham số item: Vì bạn đã khai báo nó trong hàm là kiểu dữ liệu Item
nên bạn cũng sẽ có mọi hỗ trợ của trình soạn thảo (hoàn thành, v.v.) cho tất cả các thuộc tính và kiểu dữ liệu của chúng.
'''