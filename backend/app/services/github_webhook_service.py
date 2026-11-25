from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.webhook_event import WebhookEvent
from app.schemas.github_webhook import GithubWebhookPayload


def build_github_webhook_event(
    *,
    delivery_id: str,
    event_type: str,
    payload: GithubWebhookPayload,
    raw_payload: dict,
) -> WebhookEvent:

    return WebhookEvent(
        delivery_id=delivery_id,
        event_type=event_type,
        action=payload.action,
        repo_full_name=payload.repository.full_name,
        issue_number=payload.issue.number if payload.issue else None,
        issue_title=payload.issue.title if payload.issue else None,
        sender_login=payload.sender.login,
        payload=raw_payload,
        status="received",
    )


async def save_webhook_event(
    db: AsyncSession,
    event: WebhookEvent,
) -> tuple[WebhookEvent, bool]:
    """Returns (event, created). created=False if delivery_id already existed."""
    db.add(event)
    try:
        await db.commit()
        await db.refresh(event)
        return event, True
    except IntegrityError:
        await db.rollback()
        return event, False
