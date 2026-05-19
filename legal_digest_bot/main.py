"""Entrypoint for the daily legal digest WhatsApp bot."""

from __future__ import annotations

import argparse
import logging
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler

from .config import Settings, require_user_permission
from .constants import SOURCE_URLS
from .crawler import LegalNewsItem, build_news_item, discover_candidate_links
from .pdf_report import build_pdf
from .whatsapp_sender import WhatsAppSender

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


def collect_items(settings: Settings) -> list[LegalNewsItem]:
    collected: list[LegalNewsItem] = []
    for source in SOURCE_URLS:
        try:
            links = discover_candidate_links(source, settings.max_links_per_source)
        except Exception as exc:
            logging.warning("Unable to scan source %s: %s", source, exc)
            continue

        for link in links:
            if len(collected) >= settings.articles_per_digest:
                return collected
            try:
                item = build_news_item(source, link)
            except Exception as exc:
                logging.warning("Skipping article %s due to error: %s", link, exc)
                continue
            if item:
                collected.append(item)

    return collected


def run_once(settings: Settings) -> None:
    logging.info("Starting digest run at %s", datetime.now())
    items = collect_items(settings)
    if not items:
        logging.warning("No qualifying legal items found for digest.")
        return

    pdf_path = build_pdf(items, settings.output_dir)
    logging.info("Generated PDF at %s", pdf_path)

    allowed = require_user_permission(
        "Permission request: The bot will open WhatsApp Web and send the PDF to your group"
    )
    if not allowed:
        logging.warning("Permission denied. PDF generated but not shared on WhatsApp.")
        return

    use_profile = bool(settings.chrome_profile_dir)
    if use_profile:
        profile_allowed = require_user_permission(
            "Permission request: Reuse your Chrome profile for WhatsApp login persistence"
        )
        if not profile_allowed:
            settings.chrome_profile_dir = ""

    sender = WhatsAppSender(profile_dir=settings.chrome_profile_dir)
    try:
        sender.send_pdf_to_group(settings.whatsapp_group_name, pdf_path)
        logging.info("PDF sent to WhatsApp group '%s'", settings.whatsapp_group_name)
    finally:
        sender.close()


def run_scheduler(settings: Settings) -> None:
    scheduler = BlockingScheduler(timezone=settings.timezone)
    scheduler.add_job(run_once, "cron", hour=settings.run_hour, minute=settings.run_minute, args=[settings])
    logging.info("Scheduler active. Daily run set to %02d:%02d (%s)", settings.run_hour, settings.run_minute, settings.timezone)
    scheduler.start()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Daily legal digest WhatsApp bot")
    parser.add_argument("--once", action="store_true", help="Run immediately once")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = Settings()
    if args.once:
        run_once(settings)
    else:
        run_scheduler(settings)


if __name__ == "__main__":
    main()
