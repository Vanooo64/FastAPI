from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, ConfigDict

app = FastAPI()

data = {
    "email": "abc@mail.com",
    "bio": "Привіт світ",
    "age": 12,
}

data_wo_age = {
    "email": "abc@mail.com",
    "bio": None,
    # "gender": "male",
    # "birthday": "2000"
}


class UserSchema(BaseModel):
    email: EmailStr #Перевіряє валідність email
    bio: str | None = Field(max_length=1000) # перевіряє довжину опису "bio"

    model_config = ConfigDict(extra='forbid') #Забороняє додаткові параметри окрім тих які прописані в класі


users = []

@app.post("/users")
def add_user(user: UserSchema):
    users.append(user)
    return {"ok": True, "msg": "Юзера додано"}


@app.get("/users")
def get_user() -> list[UserSchema]:
    return users


class UserAgeSchema(UserSchema): # наслідуємо від класу UserSchema яки наслідується від BaseModel
    age: int = Field(ge=0, le=130) #вік повинен бути не менше 0 і не більше 120


user = UserAgeSchema(**data)
print(repr(user)) #repr - повердає дані з назвою класу і його данними

user_wo_age = UserSchema(**data_wo_age)
print(repr(user_wo_age))

