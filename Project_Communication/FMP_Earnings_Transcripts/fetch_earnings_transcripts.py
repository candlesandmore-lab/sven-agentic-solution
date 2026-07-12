"""One-off extraction: pull batch earnings-call transcripts from FMP for a fixed ticker
list and year range, and write them to a single JSON file keyed by ticker.

Uses FMP's v4 batch endpoint (one call per ticker per year):
    https://financialmodelingprep.com/api/v4/batch_earning_call_transcript/{ticker}?year={year}&apikey=...

Loads FMP_API_KEY from the project's .env file itself (no external dotenv dependency
needed for this one-off script). Uses `truststore` to verify TLS against the Windows
certificate store instead of the `certifi` bundle -- required on this network, which
terminates TLS through a corporate proxy whose root CA is trusted by Windows but isn't
in the public CA bundle `certifi`/`uv` ship with. Run with:
    uv run --system-certs --with truststore python Project_Communication/FMP_Earnings_Transcripts/fetch_earnings_transcripts.py
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import truststore

truststore.inject_into_ssl()

import httpx

FMP_BASE_URL = "https://financialmodelingprep.com"
TICKERS = ["MU", "SNDK", "WDC", "HPQ", "DELL", "CSCO"]
YEARS = [2024, 2025, 2026]
OUTPUT_PATH = Path(__file__).parent / "earnings_transcripts.json"
ENV_PATH = Path(__file__).parent.parent.parent / ".env"


def load_env_file(path: Path) -> None:
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def fetch_transcripts_for_ticker(client: httpx.Client, api_key: str, ticker: str) -> list[dict]:
    transcripts: list[dict] = []
    for year in YEARS:
        response = client.get(
            f"/api/v4/batch_earning_call_transcript/{ticker}",
            params={"year": year, "apikey": api_key},
        )
        response.raise_for_status()
        payload = response.json()
        if isinstance(payload, list):
            transcripts.extend(payload)
    return transcripts


def main() -> None:
    if ENV_PATH.exists():
        load_env_file(ENV_PATH)

    api_key = os.environ.get("FMP_API_KEY")
    if not api_key:
        raise SystemExit(f"FMP_API_KEY is not configured (checked {ENV_PATH} and the environment).")

    results: dict[str, list[dict]] = {}
    with httpx.Client(base_url=FMP_BASE_URL, timeout=30.0) as client:
        for ticker in TICKERS:
            print(f"Fetching {ticker} ({', '.join(str(y) for y in YEARS)})...")
            results[ticker] = fetch_transcripts_for_ticker(client, api_key, ticker)
            print(f"  {len(results[ticker])} transcript(s)")

    OUTPUT_PATH.write_text(json.dumps(results, indent=2))
    print(f"\nWrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
