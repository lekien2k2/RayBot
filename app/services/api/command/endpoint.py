import logging
from typing import Optional
from fastapi import APIRouter, Query, status

from app.services.api.command import service as commandService

# from sqlalchemy.orm import Session
from app.services.api.dependencies import SessionDep

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def get_command(
    db: SessionDep,
    *,
    page: int = 1,
    limit: int = 10,
    from_date: Optional[str] = Query(None, description="From date"),
    to_date: Optional[str] = Query(None, description="To date"),
    sort_order: str = Query("desc", description="Sort order"),
):
    command, meta = commandService.get_commands(
        db,
        page=page,
        limit=limit,
        from_date=from_date,
        to_date=to_date,
        sort_order=sort_order,
    )
    return {"data": command, "meta_data": meta}
