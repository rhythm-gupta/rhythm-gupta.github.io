"""Article discovery and extraction."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
import trafilatura
from bs4 import BeautifulSoup

from .constants import ACT_KEYWORDS, COURT_KEYWORDS, PDF_HINTS

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36"


@dataclass
class LegalNewsItem:
    title: str
    article_url: str
    source: str
    court: str
    bench: str
    judges: list[str]
    summary_points: list[str]
    act_tags: list[str]
    judgment_pdf_url: str


def fetch_html(url: str, timeout: int = 20) -> str:
    response = requests.get(url, timeout=timeout, headers={"User-Agent": UA})
    response.raise_for_status()
    return response.text


def discover_candidate_links(source_url: str, limit: int) -> list[str]:
    html = fetch_html(source_url)
    soup = BeautifulSoup(html, "html.parser")
    source_host = urlparse(source_url).netloc
    links: list[str] = []

    for a in soup.select("a[href]"):
        href = urljoin(source_url, a.get("href", ""))
        text = " ".join(a.get_text(" ", strip=True).split())
        if not href.startswith("http") or len(text) < 25:
            continue
        if urlparse(href).netloc != source_host:
            continue
        if any(x in href.lower() for x in ["/tag/", "/author/", "#", "javascript:"]):
            continue
        if href not in links:
            links.append(href)
        if len(links) >= limit:
            break
    return links


def extract_article(url: str) -> tuple[str, str]:
    html = fetch_html(url)
    downloaded = trafilatura.extract(
        html,
        include_links=True,
        include_formatting=False,
        output_format="txt",
    )
    text = downloaded or BeautifulSoup(html, "html.parser").get_text(" ", strip=True)
    title = BeautifulSoup(html, "html.parser").title
    title_text = title.get_text(strip=True) if title else url
    return title_text, text


def match_court(text: str) -> str:
    lower = text.lower()
    for court, patterns in COURT_KEYWORDS.items():
        if any(p in lower for p in patterns):
            return court
    return ""


def match_acts(text: str) -> list[str]:
    lower = text.lower()
    return [act for act in ACT_KEYWORDS if act in lower]


def extract_bench_and_judges(text: str) -> tuple[str, list[str]]:
    bench_match = re.search(r"(?:bench|coram)\s*[:\-]\s*([^\n\.]{5,180})", text, flags=re.I)
    bench = bench_match.group(1).strip() if bench_match else "Not clearly stated in source"

    judge_candidates = re.findall(r"Justice\s+[A-Z][A-Za-z\.\s]+", text)
    unique_judges = []
    for judge in judge_candidates:
        judge = " ".join(judge.split())
        if judge not in unique_judges:
            unique_judges.append(judge)
    return bench, unique_judges[:6]


def find_pdf_link(article_url: str) -> str:
    html = fetch_html(article_url)
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.select("a[href]"):
        href = urljoin(article_url, a.get("href", ""))
        text = a.get_text(" ", strip=True).lower()
        if href.lower().endswith(".pdf") or any(hint in text for hint in PDF_HINTS):
            return href
    return ""


def sentence_tokenize(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 45]


def summarize_points(text: str, act_tags: Iterable[str], court: str, max_points: int = 6) -> list[str]:
    sentences = sentence_tokenize(text)
    priority_terms = [court.lower(), *[a.lower() for a in act_tags]]
    scored: list[tuple[int, str]] = []
    for sentence in sentences:
        low = sentence.lower()
        score = sum(4 for term in priority_terms if term and term in low)
        if any(k in low for k in ["held", "observed", "ruled", "directed", "clarified"]):
            score += 3
        if any(k in low for k in ["petition", "appeal", "judge", "bench"]):
            score += 1
        scored.append((score, sentence))
    scored.sort(key=lambda item: item[0], reverse=True)
    picks = [s for score, s in scored[:max_points] if score > 0]
    if not picks:
        picks = sentences[:max_points]
    return picks


def build_news_item(source: str, article_url: str) -> LegalNewsItem | None:
    title, text = extract_article(article_url)
    court = match_court(text)
    if not court:
        return None

    act_tags = match_acts(text)
    if not act_tags:
        return None

    bench, judges = extract_bench_and_judges(text)
    summary_points = summarize_points(text, act_tags, court)
    if not summary_points:
        return None

    pdf_url = find_pdf_link(article_url)
    if not pdf_url:
        query = requests.utils.quote(title)
        pdf_url = (
            f"https://indiankanoon.org/search/?formInput={query}"
            "  (Fallback: search title on Supreme Court/Delhi HC official sites)"
        )

    return LegalNewsItem(
        title=title,
        article_url=article_url,
        source=source,
        court=court,
        bench=bench,
        judges=judges,
        summary_points=summary_points,
        act_tags=act_tags,
        judgment_pdf_url=pdf_url,
    )
