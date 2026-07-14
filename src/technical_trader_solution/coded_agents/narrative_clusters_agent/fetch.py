"""FMP data provider client for the fetch node.

Calls FMP's earnings-transcript, SEC-filing, and news endpoints per ticker and normalizes
the responses into `RawDocument` records. Requires `FMP_API_KEY` to be set; callers
without a configured key should inject a fixture- or mock-backed `fetch_documents`
callable instead of constructing `FMPClient` (see tests/fixtures/narrative_clusters/).

The exact FMP endpoint paths below are this module's best-effort mapping onto FMP's
publicly documented REST API shape; verify them against a live `FMP_API_KEY` and FMP's own
current API reference before the first live nightly run, per task_5's live-endpoint QA
pass.
"""

from __future__ import annotations

import os
from collections.abc import Callable
from datetime import datetime

import httpx

from technical_trader_solution.coded_agents.narrative_clusters_agent.models import (
    RawDocument,
    SourceType,
)
from technical_trader_solution.errors import ConfigurationError, DataProviderError

FMP_BASE_URL = "https://financialmodelingprep.com"

FetchDocuments = Callable[[str, datetime | None], list[RawDocument]]


class FMPCredentialError(ConfigurationError):
    """Raised when FMP_API_KEY is required but not configured."""


class FMPClient:
    """Thin FMP REST client, normalizing responses into `RawDocument` records."""

    def __init__(
        self,
        api_key: str | None = None,
        *,
        base_url: str = FMP_BASE_URL,
        http_client: httpx.Client | None = None,
    ) -> None:
        resolved_key = api_key or os.environ.get("FMP_API_KEY")
        if not resolved_key:
            raise FMPCredentialError(
                "FMP_API_KEY is not configured. Set the environment variable, or inject a "
                "fixture-/mock-backed FetchDocuments callable instead of using FMPClient."
            )
        self.api_key = resolved_key
        self.base_url = base_url
        self._client = http_client or httpx.Client(base_url=base_url, timeout=30.0)

    def _get(self, path: str, params: dict[str, str]) -> list[dict]:
        try:
            response = self._client.get(path, params={**params, "apikey": self.api_key})
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise DataProviderError(f"FMP request to {path} failed: {exc}") from exc
        return response.json()

    def fetch_earnings_transcripts(
        self, ticker: str, since: datetime | None = None
    ) -> list[RawDocument]:
        payload = self._get(f"/api/v4/earning_call_transcript/{ticker}", {})
        return [
            RawDocument(
                ticker=ticker,
                source_type=SourceType.EARNINGS_TRANSCRIPT,
                source_id=f"{ticker}-transcript-{item.get('quarter')}-{item.get('year')}",
                published_at=_parse_datetime(item.get("date")),
                text=item.get("content", ""),
            )
            for item in payload
            if _after(since, _parse_datetime(item.get("date")))
        ]

    def fetch_sec_filings(self, ticker: str, since: datetime | None = None) -> list[RawDocument]:
        payload = self._get("/api/v3/sec_filings", {"symbol": ticker})
        return [
            RawDocument(
                ticker=ticker,
                source_type=SourceType.SEC_FILING,
                source_id=item.get("finalLink", item.get("cik", "")),
                published_at=_parse_datetime(item.get("fillingDate") or item.get("acceptedDate")),
                text=item.get("type", "") + " " + item.get("finalLink", ""),
            )
            for item in payload
            if _after(since, _parse_datetime(item.get("fillingDate") or item.get("acceptedDate")))
        ]

    def fetch_news(self, ticker: str, since: datetime | None = None) -> list[RawDocument]:
        payload = self._get("/api/v3/stock_news", {"tickers": ticker})
        return [
            RawDocument(
                ticker=ticker,
                source_type=SourceType.NEWS,
                source_id=item.get("url", ""),
                published_at=_parse_datetime(item.get("publishedDate")),
                text=(item.get("title", "") + ". " + item.get("text", "")).strip(),
            )
            for item in payload
            if _after(since, _parse_datetime(item.get("publishedDate")))
        ]

    def fetch_documents(self, ticker: str, since: datetime | None = None) -> list[RawDocument]:
        """Fetch all three source types for `ticker`, published after `since`."""

        return [
            *self.fetch_earnings_transcripts(ticker, since),
            *self.fetch_sec_filings(ticker, since),
            *self.fetch_news(ticker, since),
        ]


def _parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.min
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            continue
    return datetime.fromisoformat(value)


def _after(since: datetime | None, published_at: datetime) -> bool:
    return since is None or published_at > since
