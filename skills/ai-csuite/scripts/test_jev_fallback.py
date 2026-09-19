"""Adversarial check: every Jev failure mode must fall back, never crash."""
import http.client
import io
import json
import socket
import ssl
import sys
import urllib.error
import urllib.request

import pathlib  # noqa: E402

SCRIPTS = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))
import jev  # noqa: E402
import run_debate  # noqa: E402
from common import load_company  # noqa: E402

COMPANY = load_company(SCRIPTS.parent / "config" / "company.yaml")
TOPIC = "Should we raise prices?"


class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


def body(payload):
    def f(req, timeout=None):
        return Resp(json.dumps(payload).encode())
    return f


def raises(exc):
    def f(req, timeout=None):
        raise exc
    return f


CASES = {
    # network-layer
    "dns failure":        raises(urllib.error.URLError("nodename nor servname provided")),
    "timeout":            raises(TimeoutError("timed out")),
    "socket.timeout":     raises(socket.timeout("timed out")),
    "connection refused": raises(ConnectionRefusedError(61, "Connection refused")),
    "connection reset":   raises(ConnectionResetError(54, "Connection reset by peer")),
    "broken pipe":        raises(BrokenPipeError(32, "Broken pipe")),
    "remote disconnect":  raises(http.client.RemoteDisconnected("closed")),
    "incomplete read":    raises(http.client.IncompleteRead(b"partial")),
    "ssl error":          raises(ssl.SSLError("handshake failed")),
    # HTTP status
    "401 bad key":        raises(urllib.error.HTTPError("u", 401, "Unauthorized", {}, None)),
    "429 rate limited":   raises(urllib.error.HTTPError("u", 429, "Too Many Requests", {}, None)),
    "500 server error":   raises(urllib.error.HTTPError("u", 500, "Server Error", {}, None)),
    # malformed payloads
    "not json":           lambda r, timeout=None: Resp(b"<html>502 Bad Gateway</html>"),
    "invalid utf8":       lambda r, timeout=None: Resp(b"\xff\xfe\x00bad"),
    "empty body":         lambda r, timeout=None: Resp(b""),
    "json null":          body(None),
    "json list":          body([1, 2, 3]),
    "no answers key":     body({"model": "jev-1.13.0"}),
    "answers is string":  body({"answers": "oops"}),
    "answers empty":      body({"answers": {}}),
    "missing question":   body({"answers": {"consensus": {"choice": "x", "confidence": 0.9}}}),
    "choice missing key": body({"answers": {k: {} for k in
                          ["consensus", "reversibility", "confidence",
                           "legal_risk", "runway_risk", "customer_contradiction",
                           "deadlock", "groupthink"]}}),
}

NOULS = {k: {"noul": 0.5} for k in
         ["legal_risk", "runway_risk", "customer_contradiction", "deadlock", "groupthink"]}


def partial(score):
    return body({"answers": {
        "consensus": {"choice": "x", "confidence": 0.9},
        "reversibility": {"choice": "irreversible"},
        "confidence": {"score": score},
        **NOULS,
    }})


CASES["score is null"] = partial(None)
CASES["score is string"] = partial("high")
CASES["noul is string"] = body({"answers": {
    "consensus": {"choice": "x", "confidence": 0.9},
    "reversibility": {"choice": "irreversible"},
    "confidence": {"score": 2.0},
    **{k: {"noul": "yes"} for k in NOULS},
}})

BASELINE = run_debate.build_output(
    TOPIC, COMPANY, ["CEO", "CTO", "CPO", "CFO", "CoS"], 2, "pricing", use_jev=False
)

orig = urllib.request.urlopen
fails = []
for name, stub in CASES.items():
    urllib.request.urlopen = stub
    try:
        cat = jev.classify_topic(TOPIC, COMPANY)
        out = run_debate.build_output(
            TOPIC, COMPANY, ["CEO", "CTO", "CPO", "CFO", "CoS"], 2, cat or "pricing", use_jev=True
        )
        if out != BASELINE:
            fails.append(f"{name}: produced NON-BASELINE output")
        else:
            print(f"  ok       {name}")
    except Exception as e:
        fails.append(f"{name}: CRASHED {type(e).__name__}: {e}")
        print(f"  CRASH    {name}: {type(e).__name__}")
urllib.request.urlopen = orig

print()
if fails:
    print(f"FAIL ({len(fails)}/{len(CASES)})")
    for f in fails:
        print(f"  - {f}")
    sys.exit(1)
print(f"PASS — all {len(CASES)} failure modes fell back to identical baseline output")
