from __future__ import annotations

from apscheduler.schedulers.background import BackgroundScheduler


scheduler = BackgroundScheduler(timezone="UTC")


def start_scheduler() -> None:
    if not scheduler.running:
        scheduler.start()


def shutdown_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
