from fastapi import FastAPI
from contextlib import asynccontextmanager

import routes
from db import create_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(routes.router, prefix="")


