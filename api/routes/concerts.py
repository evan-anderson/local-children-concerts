"""Concert API endpoints."""

from typing import Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from api.services.concert_service import get_available_towns, get_filtered_concerts

router = APIRouter(prefix="/api", tags=["concerts"])


class ConcertResponse(BaseModel):
    title: str
    venue: str
    town: str
    date: str
    url: Optional[str] = None
    description: Optional[str] = None
    address: Optional[str] = None
    source: Optional[str] = None
    scraped_at: str


class ConcertsListResponse(BaseModel):
    concerts: list[ConcertResponse]
    total: int
    last_updated: Optional[str] = None


@router.get("/concerts", response_model=ConcertsListResponse)
async def get_concerts(
    towns: Optional[list[str]] = Query(None, description="Filter by towns"),
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
) -> ConcertsListResponse:
    """Get filtered concerts."""
    concerts = get_filtered_concerts(towns, start_date, end_date)
    # Get last_updated from first concert's scraped_at (all scraped together)
    last_updated = concerts[0]["scraped_at"] if concerts else None
    return ConcertsListResponse(
        concerts=[ConcertResponse(**c) for c in concerts],
        total=len(concerts),
        last_updated=last_updated,
    )


@router.get("/towns", response_model=list[str])
async def get_towns() -> list[str]:
    """Get list of available towns for filtering."""
    return get_available_towns()


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
