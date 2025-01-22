import uvicorn as uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Асинхронність в python",
        "author": "Метью",
    },
    {
        "id": 2,
        "title": "Backend в python",
        "author": "Іван",
    },
]


@app.get(
    "/books",
    tags=['Книги'],
    summary="Отримати усі книги")
def read_books():
    return books


@app.get(
    "/books/{book_id}",
    tags=["Книги"],
    summary="Отримати конкретну книгу по ID")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Книга не знайдена")


class NewBook(BaseModel):
    title: str
    author: str


@app.post("/books")
def create_book(new_book: NewBook):
    books.append({
        "id": len(books) + 1,
        "title":new_book.title,
        "author":new_book.author
    })
    return {"success": True, "massage": "Книга успішно додана"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
