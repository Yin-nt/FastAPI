from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
'''
- Client gửi 1 yêu cầu đến ỦL 'tôken' với username và password
- Máy chủ xác minh thông tin đăng nhập, nếu chính xác nó sẽ tạo 1 token
- Client bao gồm token này trong tiêu đề Authorization cho các yên cầu tiếp theo để truy cập các route được bảo vệ 
'''
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]): #read_items được bảo vệ xác thực bởi OAuth2
    return {"token": token}
