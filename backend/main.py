from fastapi import FastAPI

from router.router import router as main_router

app: FastAPI = FastAPI(description="Backend REST API for Slavens Tennis Website")

app.include_router(main_router)
