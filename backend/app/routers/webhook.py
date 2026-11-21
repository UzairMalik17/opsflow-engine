from fastapi import APIRouter

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.get("/ping")
async def webhook_router_test() -> dict[str, str]:
    return {"message": "webhook router is running"}
