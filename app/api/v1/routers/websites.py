from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.website import Website, WebsiteCheck
from app.core.database import get_async_session
from app.api.v1.schemas.website import (
    WebsiteCreate,
    WebsiteUpdate,
    WebsiteRead,
    WebsiteCheckRead,
)
from app.utils.normalization import normalize_url
from app.utils.ssrf_guard import host_is_private
from time import perf_counter
import httpx

router = APIRouter(prefix="/api/v1/websites", tags=["websites"])


async def perform_http_check(url: str):
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        start = perf_counter()
        resp = await client.get(url)
        duration_ms = int((perf_counter() - start) * 1000)
        code = resp.status_code
        status_val = "UP" if 200 <= code < 400 else "DOWN"
        return status_val, code, duration_ms, None


async def create_check_record(
    session: AsyncSession, website_id, status, code, resp_time, err
):
    check = WebsiteCheck(
        website_id=website_id,
        status=status,
        http_code=code,
        response_time_ms=resp_time,
        error=err,
    )
    session.add(check)
    await session.commit()
    await session.refresh(check)
    return check


@router.post("/", response_model=WebsiteRead)
async def create_website(
    data: WebsiteCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        data.url = normalize_url(data.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    result = await session.exec(select(Website).where(Website.url == data.url))
    existing = result.first()
    if existing:
        raise HTTPException(status_code=400, detail="Website already exists")

    site = Website(name=data.name, url=data.url)
    session.add(site)
    await session.commit()
    await session.refresh(site)
    return site


@router.get("/", response_model=list[WebsiteRead])
async def list_websites(session: AsyncSession = Depends(get_async_session)):
    result = await session.exec(select(Website))
    return result.all()


@router.get("/{website_id}", response_model=WebsiteRead)
async def get_website(
    website_id: int, session: AsyncSession = Depends(get_async_session)
):
    site = await session.get(Website, website_id)
    if not site:
        raise HTTPException(status_code=404, detail="Website not found")
    return site


@router.patch("/{website_id}", response_model=WebsiteRead)
async def update_website(
    website_id: int,
    data: WebsiteUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    site = await session.get(Website, website_id)
    if not site:
        raise HTTPException(status_code=404, detail="Website not found")

    if data.url:
        try:
            data.url = normalize_url(data.url)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(site, key, value)

    session.add(site)
    await session.commit()
    await session.refresh(site)
    return site


@router.post("/{website_id}/check", response_model=WebsiteCheckRead)
async def manual_check(
    website_id: int, session: AsyncSession = Depends(get_async_session)
):
    w = await session.get(Website, website_id)
    if not w:
        raise HTTPException(status_code=404, detail="Website not found")

    host = httpx.URL(w.url).host
    if await host_is_private(host):
        await create_check_record(session, w.id, "UNKNOWN", None, None, "SSRF blocked")
        raise HTTPException(status_code=400, detail="SSRF blocked")

    try:
        status_val, code, resp_time, err = await perform_http_check(w.url)
    except Exception as exc:
        status_val, code, resp_time, err = "DOWN", None, None, str(exc)

    chk = await create_check_record(session, w.id, status_val, code, resp_time, err)
    return chk
