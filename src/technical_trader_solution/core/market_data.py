"""FMP historical-price client for the Discovery Surface's side-by-side chart view.

Same FMP data provider already approved for narrative/topic ingestion (see
docs/implementation/01-narrative-cluster-discovery-surface.md, Discovery Surface and
Dependencies) -- this module only adds its historical-price endpoint, not a new external
dependency. Kept independent of the narrative_clusters coded agent's own FMPClient so
`core` stays the shared foundation other surfaces (here, the dashboard) build on directly,
per the package-layout sub-skill.
"""

from __future__ import annotations

import os

import httpx
from pydantic import BaseModel

FMP_BASE_URL = "https://financialmodelingprep.com"


class FMPCredentialError(RuntimeError):
    """Raised when FMP_API_KEY is required but not configured."""


class PricePoint(BaseModel):
    """One historical daily close for a ticker."""

    date: str
    close: float


def fetch_historical_prices(
    ticker: str,
    *,
    api_key: str | None = None,
    base_url: str = FMP_BASE_URL,
    http_client: httpx.Client | None = None,
) -> list[PricePoint]:
    """This ticker's daily closes from FMP's historical price endpoint, oldest first."""

    resolved_key = api_key or os.environ.get("FMP_API_KEY")
    if not resolved_key:
        raise FMPCredentialError(
            "FMP_API_KEY is not configured. Set the environment variable to enable "
            "chart-inspection price data."
        )
    client = http_client or httpx.Client(base_url=base_url, timeout=30.0)
    response = client.get(
        f"/api/v3/historical-price-full/{ticker}", params={"apikey": resolved_key}
    )
    response.raise_for_status()
    payload = response.json()
    history = payload.get("historical", [])
    points = [
        PricePoint(date=item["date"], close=item["close"])
        for item in history
        if "date" in item and "close" in item
    ]
    return list(reversed(points))
