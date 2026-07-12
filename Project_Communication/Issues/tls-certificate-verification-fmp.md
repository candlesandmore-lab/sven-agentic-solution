# TLS certificate verification fails for external HTTPS calls (FMP, PyPI)

## Issue

Any Python HTTPS request to an external host (e.g. `financialmodelingprep.com`,
`pypi.org`) made from this machine/network fails during the TLS handshake:

```
httpx.ConnectError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed:
unable to get local issuer certificate (_ssl.c:1010)
```

`uv` itself hits the same failure fetching packages from PyPI:

```
error sending request for url (https://pypi.org/simple/truststore/)
invalid peer certificate: UnknownIssuer
```

Meanwhile plain `curl` (Windows `schannel` backend) reaches the same hosts fine at the
handshake level, only failing later on a revocation check (`CRYPT_E_NO_REVOCATION_CHECK`),
and `https://www.google.com` works over `curl` without issue.

## Root cause

This network terminates outbound TLS through a corporate inspection proxy. Its root CA
is installed in the **Windows certificate store** (which `curl`/`schannel` consults), but
is **not** present in the public CA bundles that Python's `certifi` package and `uv`
ship with. Anything that verifies certificates against `certifi` (Python's `ssl` module
by default, `httpx`, `requests`, `uv`'s own downloader) therefore cannot build a trust
chain to the proxy's re-signed certificate and fails immediately with
`unable to get local issuer certificate` / `UnknownIssuer`.

This is host/network-specific, not code-specific: any script making a live HTTPS call
from this machine hits it, including this project's own `FMPClient` /
`core/market_data.py`, which had never actually been exercised against the live FMP
endpoint before (they're normally used with fixture-/mock-backed callables and the
`live_endpoint`-marked test is opt-in).

## Solution

Use the [`truststore`](https://pypi.org/project/truststore/) package to make Python's
`ssl` module verify against the OS-native certificate store (Windows cert store here)
instead of `certifi`:

```python
import truststore
truststore.inject_into_ssl()

import httpx  # import HTTP libraries after injecting
```

Since `uv` needs network access to fetch `truststore` itself the first time, pass
`--system-certs` so `uv`'s own downloader also trusts the OS store:

```powershell
uv run --system-certs --with truststore python <script.py>
```

After this, TLS handshakes to `financialmodelingprep.com` succeed (verified via a live
request that returned a normal `401 Invalid API KEY` HTTP response rather than a TLS
error).

## Applies to

- `Project_Communication/FMP_Earnings_Transcripts/fetch_earnings_transcripts.py` (fixed)
- Any future one-off script making live external HTTPS calls from this machine
- Potentially relevant to `technical_trader_solution`'s `FMPClient` /
  `core/market_data.py` if/when they're run against the live endpoint (currently only
  exercised via fixtures/mocks, per `fetch.py`'s docstring and the `live_endpoint` pytest
  marker) from this same network — worth checking before the planned live-endpoint QA
  pass.
