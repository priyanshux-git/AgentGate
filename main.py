import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from olostep import AsyncOlostep

from api_test import test

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncOlostep(api_key=os.environ["OLOSTEP_API_KEY"]) as client:
        app.state.olostep = client
        yield


app = FastAPI(lifespan=lifespan)

app.include_router(test)
