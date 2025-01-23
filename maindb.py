from typing import Annotated

from fastapi import FastAPI, Depends
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, \
    AsyncSession  # create_async_engine - асинхронний двигун для підключення до бази даних.
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()
# async_sessionmaker: Створює асинхронні сесії для виконання запитів до бази даних.
engine = create_async_engine('sqlite+aiosqlite:///books.db') # створеня БД

new_session = async_sessionmaker(engine, expire_on_commit=False) # Створює фабрику асинхронних сесій.

async def get_session(): # асинхронним генератором, який відкриває нову сесію для виконання запитів до бази даних
    async with new_session() as session:
        yield session #yield, функція повертає значення, але не завершує своє виконання.


SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass


class BookModel(Base):
    """створення каркасу таблиці """
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:  # Відкриття асинхронного з'єднання до БД
        await conn.run_sync(Base.metadata.drop_all) #очищення БД
        await conn.run_sync(Base.metadata.create_all) # Створення таблиць для БД
    return {"ok": True}

class BookAddSchema(BaseModel):
    title: str
    author: str


class BookSchema(BookAddSchema):
    id: int

@app.post("/books")
async def add_book(data: BookSchema, session:SessionDep):
    new_book = BookModel(
        title=data.title,
        author=data.author,
    )
    session.add(new_book)
    await session.commit()
    return {"ok": True}

@app.get("/books")
async def get_books(session:SessionDep):
    query = select(BookModel)
    result = await session.execute(query)
    return result.scalars().all()




