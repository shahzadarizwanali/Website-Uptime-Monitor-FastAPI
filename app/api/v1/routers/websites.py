from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models.website import Website
from app.core.database import get_session
from app.api.v1.schemas import WebsiteCreate, WebsiteUpdate
from app.utils import normalize_url


router = APIRouter(prefix="/api/v1/websites", tags=["websites"])


@router.post("/")
def create_website(data: WebsiteCreate, session: Session = Depends(get_session)):
    if not normalize_url(data.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    existing = session.exec(select(Website).where(Website.url == data.url)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Website already exists")

    site = Website(name=data.name, url=data.url)
    session.add(site)
    session.commit()
    session.refresh(site)
    return site


@router.get("/")
def list_websites(session: Session = Depends(get_session)):
    return session.exec(select(Website)).all()


@router.get("/{website_id}")
def get_website(website_id: int, session: Session = Depends(get_session)):
    site = session.get(Website, website_id)
    if not site:
        raise HTTPException(status_code=404, detail="Website not found")
    return site


@router.patch("/{website_id}")
def update_website(
    website_id: int, data: WebsiteUpdate, session: Session = Depends(get_session)
):
    site = session.get(Website, website_id)
    if not site:
        raise HTTPException(status_code=404, detail="Website not found")

    if data.url and not normalize_url(data.url):
        raise HTTPException(status_code=400, detail="Invalid URL")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(site, key, value)

    session.add(site)
    session.commit()
    session.refresh(site)
    return site
