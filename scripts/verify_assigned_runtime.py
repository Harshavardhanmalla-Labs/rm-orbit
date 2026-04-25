#!/usr/bin/env python3

import argparse
import socket
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple


@dataclass(frozen=True)
class ServicePort:
    name: str
    port: int
    path: str = "/"


FRONTEND_PORTS: Sequence[ServicePort] = (
    ServicePort("Gate", 45001),
    ServicePort("Meet", 45003),
    ServicePort("Mail", 45004),
    ServicePort("Calendar", 45005),
    ServicePort("Planet", 45006),
    ServicePort("Fonts", 45007),
    ServicePort("Connect", 45008),
    ServicePort("Learn", 45009),
    ServicePort("Writer", 45010),
    ServicePort("Control Center", 45011),
    ServicePort("Secure", 45012),
    ServicePort("Capital Hub", 45013),
    ServicePort("Atlas", 5173),
)


BACKEND_PORTS: Sequence[ServicePort] = (
    ServicePort("Connect API", 5000),
    ServicePort("Calendar API", 5001),
    ServicePort("Meet API", 6001),
    ServicePort("Snitch Learn", 6002),
    ServicePort("Snitch Capital Hub", 6003),
    ServicePort("Snitch Secure", 6004),
    ServicePort("Snitch EventBus", 6005),
    ServicePort("Snitch Media", 6006),
    ServicePort("Writer API", 6011),
    ServicePort("Search API", 6200),
    ServicePort("Atlas API", 8000),
    ServicePort("Mail API", 8004),
    ServicePort("Control Center API", 8077),
    ServicePort("Planet API", 46000),
)


def check_tcp_open(port: int, timeout: float) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(timeout)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def check_http_code(port: int, path: str, timeout: float) -> int:
    url = f"http://127.0.0.1:{port}{path}"
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return int(resp.status)
    except urllib.error.HTTPError as err:
        return int(err.code)
    except Exception:
        return 0


def run_checks(ports: Iterable[ServicePort], timeout: float) -> Tuple[List[str], List[Tuple[str, int, str, str]]]:
    failures: List[str] = []
    rows: List[Tuple[str, int, str, str]] = []
    for svc in ports:
        tcp_open = check_tcp_open(svc.port, timeout)
        http_code = check_http_code(svc.port, svc.path, timeout) if tcp_open else 0
        tcp_text = "OPEN" if tcp_open else "CLOSED"
        http_text = str(http_code) if http_code else "NOHTTP"
        rows.append((svc.name, svc.port, tcp_text, http_text))
        if not tcp_open:
            failures.append(f"{svc.name} ({svc.port}) TCP closed")
            continue
        if http_code == 0:
            failures.append(f"{svc.name} ({svc.port}) no HTTP response")
    return failures, rows


def print_table(title: str, rows: Sequence[Tuple[str, int, str, str]]) -> None:
    print(title)
    print("SERVICE\tPORT\tTCP\tHTTP")
    for name, port, tcp, http in rows:
        print(f"{name}\t{port}\t{tcp}\t{http}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate assigned RM Orbit runtime ports.")
    parser.add_argument(
        "--frontend-only",
        action="store_true",
        help="Validate only assigned frontend ports.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=2.5,
        help="Per-check timeout in seconds (default: 2.5).",
    )
    args = parser.parse_args()

    frontend_failures, frontend_rows = run_checks(FRONTEND_PORTS, args.timeout)
    print_table("Assigned Frontend Ports", frontend_rows)

    backend_failures: List[str] = []
    backend_rows: List[Tuple[str, int, str, str]] = []
    if not args.frontend_only:
        backend_failures, backend_rows = run_checks(BACKEND_PORTS, args.timeout)
        print("")
        print_table("Core Backend Ports", backend_rows)

    failures = frontend_failures + backend_failures
    if failures:
        print("")
        print("Assigned runtime validation failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("")
    print("Assigned runtime validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
