from fastapi import FastAPI, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"  # Секретний ключ для підпису токенів JWT
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"  # Назва cookie, де зберігається токен
config.JWT_TOKEN_LOCATION = ["cookies"]  # Локація, звідки отримується токен (у цьому випадку — cookie)

security = AuthX(config=config) #Ініціалізація AuthX

class UserLoginSchema(BaseModel): # Схема даних для входу
    username: str
    password: str


@app.post('/login') #Маршрут для входу
def login(creds: UserLoginSchema ,response: Response):
    if creds.username == "test" and creds.password == ("test"): #Перевірка: якщо username і password правильні, створюється JWT токен
        token = security.create_access_token(uid='12345')
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token) #Токен додається в cookie
        return {"access_token": token}
    raise HTTPException(status_code=401, detail = "Некоректние імя чи пароль")

@app.get('/protected', dependencies=[Depends(security.access_token_required)])
def protected():
    return {'data': "TOP SECRET"}
