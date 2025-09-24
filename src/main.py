from src.config.settings import Settings
from src.api.routes.v1.orders import router as orders_router

from fastapi import FastAPI
import uvicorn

app = FastAPI()

app.include_router(orders_router, prefix="/api/v1")

settings = Settings()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.RELOAD,
    )
