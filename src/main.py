from fastapi import FastAPI

from src.api import router

app = FastAPI(title='FastAPI Onion Architecture')

app.include_router(router, prefix='/api')
