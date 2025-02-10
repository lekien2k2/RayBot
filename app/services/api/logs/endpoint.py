import logging
from typing import Optional
from fastapi import APIRouter, Query, status

from app.services.api.logs import service as LogService

# from sqlalchemy.orm import Session
from app.services.api.dependencies import SessionDep

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
def get_logs(
    db: SessionDep,
    *,
    page: int = 1,
    limit: int = 10,
    from_date: Optional[str] = Query(None, description="From date"),
    to_date: Optional[str] = Query(None, description="To date"),
    sort_order: str = Query("desc", description="Sort order"),
):
    logs, meta = LogService.get_logs(
        db,
        page=page,
        limit=limit,
        from_date=from_date,
        to_date=to_date,
        sort_order=sort_order,
    )
    return {"data": logs, "meta_data": meta}
