from typing import Annotated, Union

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

# UserInDB: Một lớp kế thừa từ User và thêm thuộc tính hashed_password
class UserInDB(User):
    hashed_password: str
#  Hàm này tìm kiếm người dùng trong cơ sở dữ liệu giả lập và trả về đối tượng UserInDB nếu tìm thấy
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
# Hàm này giả lập giải mã token và trả về thông tin người dùng từ cơ sở dữ liệu giả lập
def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

#Nếu không tìm thấy người dùng, ném ra ngoại lệ HTTP 401
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
'''
Scope: 
    - Trong OAuth2, "scope" chỉ là một chuỗi khai báo quyền cụ thể cần có.
    - Không quan trọng nếu nó có các ký tự khác như :hoặc nếu nó là một URL.
    - Đối với OAuth2, chúng chỉ là chuỗi.
Mã để lấy user và password:
    - OAuth2 yêu cầu một trường grant_typecó giá trị cố định là password, nhưng OAuth2PasswordRequestForm không bắt buộc
Hash password:
    -"Hass" có nghĩa là: chuyển đổi một số nội dung (trong trường hợp này là mật khẩu) thành một chuỗi byte (chỉ là một 
    chuỗi) trông giống như chữ vô nghĩa.
    - Không thể chuyển đổi chuỗi ký tự vô nghĩa thành mật khẩu 
    => bảo mật 





'''