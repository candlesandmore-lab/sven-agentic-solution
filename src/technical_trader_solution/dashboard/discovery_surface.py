"""Discovery Surface dashboard page (story 001, US-015).

Launched via `tts dashboard serve` (``streamlit run <this file> -- --db-path ...
--log-file ... --log-level ...``). Calls only the narrative_clusters SDK functions
(`get_clusters`, `get_cluster_trend`) for all cluster data, per the Discovery Surface's
SDK-only data-access contract in
docs/implementation/01-narrative-cluster-discovery-surface.md -- this module never
queries NarrativeClustersStore/SQLite directly. Member-ticker price charts are sourced
separately from FMP's historical price endpoint via
`technical_trader_solution.core.market_data`, per the same spec section.

Theme creation is never offered here: this page only supports chart inspection so the
human trader can make that discretionary call themselves, per STR-011.
"""

from __future__ import annotations

import argparse
import sys

import plotly.graph_objects as go
import streamlit as st

from technical_trader_solution.coded_agents.narrative_clusters_agent.storage import (
    DEFAULT_DB_PATH,
)
from technical_trader_solution.core.market_data import (
    FMPCredentialError,
    fetch_historical_prices,
)
from technical_trader_solution.logging import (
    DEFAULT_LOG_FILE,
    DEFAULT_LOG_LEVEL,
    configure_logger,
)
from technical_trader_solution.sdk.narrative_clusters import get_cluster_trend, get_clusters


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db-path", default=str(DEFAULT_DB_PATH))
    parser.add_argument("--log-file", default=DEFAULT_LOG_FILE)
    parser.add_argument("--log-level", default=DEFAULT_LOG_LEVEL)
    known_args, _ = parser.parse_known_args(sys.argv[1:])
    return known_args


@st.cache_resource
def _logger(log_file: str, log_level: str):
    return configure_logger(
        "technical_trader_solution.dashboard", log_file=log_file, log_level=log_level
    )


args = _parse_args()
logger = _logger(args.log_file, args.log_level)

st.set_page_config(page_title="Discovery Surface", layout="wide")
st.title("Discovery Surface")
st.caption(
    "Narrative clusters grouped by shared or overlapping topic, independent of "
    "pair-bond, sync, or existing theme status. Select a cluster to inspect its "
    "members' charts side by side; theme creation remains your own discretionary call "
    "after inspection (STR-011)."
)

try:
    clusters = get_clusters(db_path=args.db_path)
except Exception:
    logger.exception("Failed to load clusters for the Discovery Surface page")
    st.error("Could not load clusters. Check the dashboard log file for details.")
    clusters = []

if not clusters:
    st.info("No clusters found for the most recent run.")

if "selected_cluster_id" not in st.session_state:
    st.session_state.selected_cluster_id = None

for cluster in clusters:
    with st.container(border=True):
        header_col, action_col = st.columns([4, 1])
        with header_col:
            st.subheader(cluster.topic_label)
            st.write(
                f"**Cluster** `{cluster.cluster_id}` · **Members:** "
                f"{', '.join(cluster.member_tickers)}"
            )
            st.write(
                f"Frequency of mention: {cluster.frequency_of_mention} · "
                f"Company breadth: {cluster.company_breadth} · Run date: {cluster.run_date}"
            )
        with action_col:
            if st.button("Inspect charts", key=f"inspect-{cluster.cluster_id}"):
                st.session_state.selected_cluster_id = cluster.cluster_id

        try:
            trend = get_cluster_trend(cluster.cluster_id, db_path=args.db_path)
        except Exception:
            logger.exception("Failed to load trend for cluster %s", cluster.cluster_id)
            trend = []

        if trend:
            sparkline = go.Figure()
            sparkline.add_trace(
                go.Scatter(
                    x=[snapshot["run_date"] for snapshot in trend],
                    y=[snapshot["frequency_of_mention"] for snapshot in trend],
                    mode="lines+markers",
                    name="Frequency of mention",
                )
            )
            sparkline.update_layout(
                height=150,
                margin={"l": 10, "r": 10, "t": 10, "b": 10},
                showlegend=False,
            )
            st.plotly_chart(
                sparkline, use_container_width=True, key=f"sparkline-{cluster.cluster_id}"
            )

selected_cluster = next(
    (c for c in clusters if c.cluster_id == st.session_state.selected_cluster_id), None
)

if selected_cluster is not None:
    st.divider()
    st.header(f"Chart inspection: {selected_cluster.topic_label}")
    member_tickers = selected_cluster.member_tickers
    columns = st.columns(len(member_tickers)) if member_tickers else []
    for ticker, column in zip(member_tickers, columns):
        with column:
            st.subheader(ticker)
            try:
                prices = fetch_historical_prices(ticker)
            except FMPCredentialError:
                st.warning("FMP_API_KEY is not configured; cannot load price history.")
                continue
            except Exception:
                logger.exception("Failed to load price history for %s", ticker)
                st.warning(f"Could not load price history for {ticker}.")
                continue
            if not prices:
                st.info("No price history available.")
                continue
            price_chart = go.Figure()
            price_chart.add_trace(
                go.Scatter(
                    x=[point.date for point in prices],
                    y=[point.close for point in prices],
                    mode="lines",
                    name=ticker,
                )
            )
            price_chart.update_layout(height=300, margin={"l": 10, "r": 10, "t": 30, "b": 10})
            st.plotly_chart(price_chart, use_container_width=True, key=f"price-{ticker}")
