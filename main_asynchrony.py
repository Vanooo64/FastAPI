import time
import asyncio

from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

def sync_task():
    time.sleep(3)
    print("Email відправлено")

async def async_task():
    await asyncio.sleep(3)
    print("Зроблений запит в сторону API")


@app.post("/")
async def some_route(bg_tasks: BackgroundTasks):
    ...
    # asyncio.create_task(sync_task())
    bg_tasks.add_task(sync_task)
    return {"OK": True}

