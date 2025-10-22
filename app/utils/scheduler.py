import asyncio
from datetime import datetime, timezone
from sqlmodel import select, desc
import httpx
from app.core.database import get_async_session
from app.models.website import Website, WebsiteCheck
from app.core.config import settings
from app.api.v1.routers.websites import perform_http_check
from app.utils.ssrf_guard import host_is_private


async def background_loop():
    while True:
        async with get_async_session() as session:
            q = select(Website).where(Website.is_active)
            r = await session.exec(q)
            sites = r.scalars().all()

            now = datetime.now(timezone.utc)

            for site in sites:
                latest_q = (
                    select(WebsiteCheck)
                    .where(WebsiteCheck.website_id == site.id)
                    .order_by(desc(WebsiteCheck.checked_at))
                    .limit(1)
                )
                lr = await session.exec(latest_q)
                latest = lr.one_or_none()

                age = (
                    (now - latest.checked_at).total_seconds()
                    if latest
                    else float("inf")
                )

                if age < site.check_interval_sec:
                    continue

                host = httpx.URL(site.url).host
                if await host_is_private(host):
                    chk = WebsiteCheck(
                        website_id=site.id,
                        status="UNKNOWN",
                        http_code=None,
                        response_time_ms=None,
                        error="SSRF blocked",
                    )
                    session.add(chk)
                    await session.commit()
                    continue

                try:
                    status_val, code, resp_ms, err = await perform_http_check(site.url)
                except Exception as exc:
                    status_val, code, resp_ms, err = "DOWN", None, None, str(exc)

                chk = WebsiteCheck(
                    website_id=site.id,
                    status=status_val,
                    http_code=code,
                    response_time_ms=resp_ms,
                    error=err,
                )
                session.add(chk)
                await session.commit()

        await asyncio.sleep(settings.GLOBAL_CHECK_INTERVAL)
