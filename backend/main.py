from fastapi import FastAPI

from router.router import router as main_router

from logger import logging_service

app: FastAPI = FastAPI(description="Backend REST API for Slavens Tennis Website")


@app.on_event("startup")
async def start() -> None:
    logging_service()

app.include_router(main_router)
