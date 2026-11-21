from fastapi import APIRouter, FastAPI

from app.routers.webhook import router as webhook_router

app = FastAPI(title="OpsFlow Engine")

api_router = APIRouter(prefix="/api")
api_router.include_router(webhook_router)

app.include_router(api_router)


@app.get("/ping")
async def main_test() -> dict[str, str]:
    return {"message": "main is running"}
