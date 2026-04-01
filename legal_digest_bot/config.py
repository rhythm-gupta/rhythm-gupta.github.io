"""Runtime configuration helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    whatsapp_group_name: str = os.getenv("WHATSAPP_GROUP_NAME", "DHJS")
    run_hour: int = int(os.getenv("RUN_HOUR", "8"))
    run_minute: int = int(os.getenv("RUN_MINUTE", "0"))
    timezone: str = os.getenv("TIMEZONE", "Asia/Kolkata")
    max_links_per_source: int = int(os.getenv("MAX_LINKS_PER_SOURCE", "25"))
    articles_per_digest: int = int(os.getenv("ARTICLES_PER_DIGEST", "15"))
    output_dir: str = os.getenv("OUTPUT_DIR", "legal_digest_bot/output")
    chrome_profile_dir: str = os.getenv("CHROME_PROFILE_DIR", "")


def require_user_permission(prompt: str) -> bool:
    """Explicit user-consent gate before sensitive operations."""
    answer = input(f"{prompt} (yes/no): ").strip().lower()
    return answer in {"y", "yes"}
