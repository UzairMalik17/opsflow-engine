from typing import Annotated

from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.schemas.github_webhook import GithubWebhookPayload
from app.services.github_webhook_service import (
    build_github_webhook_event,
    save_webhook_event,
)

router = APIRouter(prefix="/webhooks", tags=["webhooks"])
DbSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/ping")
async def webhook_router_test() -> dict[str, object]:
    return {"message": "webhook router is running"}


@router.post("/github")
async def github_webhook_handler(
    payload: GithubWebhookPayload,
    x_github_event: Annotated[str, Header(alias="X-GitHub-Event")],
    x_github_delivery: Annotated[str, Header(alias="X-GitHub-Delivery")],
    db: DbSession,
    request: Request,
) -> dict[str, str]:
    raw_payload = await request.json()
    event = build_github_webhook_event(
        delivery_id=x_github_delivery,
        event_type=x_github_event,
        payload=payload,
        raw_payload=raw_payload,
    )
    saved_event, created = await save_webhook_event(db=db, event=event)
    return {
        "message": "GitHub webhook received successfully",
        "persisted_event_id": saved_event.id.__str__(),
        "created": "true" if created else "false",
    }
