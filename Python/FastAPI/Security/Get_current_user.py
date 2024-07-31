from typing import Annotated, Union

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# tạo lớp user với Pydantic
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

# tạo hàm giả lập giải mã token: trả về 1 đối tượng user với thông tin giả định
def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

#  Hàm này sử dụng Depends để phụ thuộc vào OAuth2 scheme để lấy token và sử dụng hàm fake_decode_token để giả lập lấy
#  thông tin người dùng từ token
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
'''
Khi người dùng gửi yêu cầu get đến '/users/me' với token xác thực => ứng dụng sử dụng hàm get_current_user để giải mã 
token và trả về thông tin người dùng hiện tại dưới dạng json
'''