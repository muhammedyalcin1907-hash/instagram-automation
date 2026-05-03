from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

from app.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


class ReelHistory(Base):
    __tablename__ = "reel_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    hook: Mapped[str] = mapped_column(String(300), nullable=False)
    script: Mapped[str] = mapped_column(Text, nullable=False)
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    caption: Mapped[str] = mapped_column(Text, nullable=False)
    hashtags: Mapped[str] = mapped_column(String(500), nullable=False)
    media_path: Mapped[str] = mapped_column(String(500), nullable=False)
    share_status: Mapped[str] = mapped_column(String(50), nullable=False, default="prepared")
    instagram_creation_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    instagram_media_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    dry_run: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def save_history(db: Session, payload: dict) -> ReelHistory:
    item = ReelHistory(**payload)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
