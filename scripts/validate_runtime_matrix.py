#!/usr/bin/env python3

import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


PortMap = Dict[str, Dict[str, Optional[int]]]


PORTS_LABEL_TO_KEY = {
    "Gate/AuthX": "gate",
    "Control Center": "control_center",
    "Calendar": "calendar",
    "Atlas": "atlas",
    "Planet": "planet",
    "Meet": "meet",
    "Fonts": "fonts",
    "Secure": "secure_frontend",
    "Capital Hub": "capital_hub_frontend",
    "Learn (Docs portal)": "learn_docs",
    "Learn": "learn_docs",
    "Writer (UI + backend baseline)": "writer",
    "Writer (UI prototype)": "writer",
    "Writer": "writer",
    "Connect": "connect",
    "Capital Hub frontend": "capital_hub_frontend",
    "Capital Hub service": "capital_hub_backend",
    "Secure frontend": "secure_frontend",
    "Secure backend": "secure_backend",
    "Secure service": "secure_backend",
    "Search backend": "search_backend",
    "TurboTick frontend": "turbotick_frontend",
    "TurboTick backend": "turbotick_backend",
    "RM Wallet frontend": "wallet_frontend",
    "RM Wallet backend": "wallet_backend",
    "RM Dock frontend": "dock_frontend",
    "RM Dock backend": "dock_backend",
    "TURN server": "turn",
}


PROFILE_A_CHECK_KEYS = [
    "gate",
    "control_center",
    "calendar",
    "atlas",
    "planet",
    "meet",
    "fonts",
    "learn_docs",
    "writer",
    "secure_frontend",
    "capital_hub_frontend",
    "connect",
]


PM2_APP_TO_TARGET = {
    "Atlas-Backend": ("atlas", "backend"),
    "Atlas-Frontend": ("atlas", "frontend"),
    "Calendar": ("calendar", "frontend"),
    "Connect": ("connect", "frontend"),
    "Planet": ("planet", "frontend"),
    "Control-Center-Backend": ("control_center", "backend"),
    "Control-Center-Frontend": ("control_center", "frontend"),
    "Meet-Backend": ("meet", "backend"),
    "Meet": ("meet", "frontend"),
    "Learn": ("learn_docs", "frontend"),
    "Writer-Backend": ("writer", "backend"),
    "Writer": ("writer", "frontend"),
    "RM-Fonts": ("fonts", "frontend"),
    "Secure-Frontend": ("secure_frontend", "frontend"),
    "Capital-Hub": ("capital_hub_frontend", "frontend"),
    "CapitalHub-Frontend": ("capital_hub_frontend", "frontend"),
    "Secure-Backend": ("secure_backend", "backend"),
    "Secure-Frontend": ("secure_frontend", "frontend"),
    "Search-Backend": ("search_backend", "backend"),
    "TurboTick-Backend": ("turbotick_backend", "backend"),
    "TurboTick-Frontend": ("turbotick_frontend", "frontend"),
    "RMWallet-Backend": ("wallet_backend", "backend"),
    "RMWallet-Frontend": ("wallet_frontend", "frontend"),
    "RMDock-Backend": ("dock_backend", "backend"),
    "RMDock-Frontend": ("dock_frontend", "frontend"),
    "Learn-Extension-Service": ("learn_docs", "backend"),
    "CapitalHub-Extension-Service": ("capital_hub_backend", "backend"),
    "Secure-Extension-Service": ("secure_backend", "backend"),
    "Meet-TURN-Server": ("turn", "backend"),
    "Meet-Media-Relay": ("meet", "backend"),
}


DEFAULT_PORT_SOURCE_BY_PM2_APP = {
    "Control-Center-Backend": "Control Center/server/src/index.ts",
    "Meet-Backend": "Meet/server/index.js",
    "CapitalHub-Extension-Service": "Capital Hub/node-extension/capitalhub-service.js",
    "Secure-Extension-Service": "Secure/node-extension/secure-service.js",
    "Learn-Extension-Service": "Learn/node-extension/learn-service.js",
}


README_EXPECTATIONS = {
    "README.md": [
        "PORTS.md",
        "./start-all.sh",
        "pm2 start ecosystem.config.cjs",
        "./runtime-matrix-gate.sh",
        "./contract-gate.sh",
    ],
    "Gate/README.md": [
        "http://localhost:45001",
    ],
    "Atlas/README.md": [
        "http://localhost:8000",
        "http://localhost:5173",
    ],
    "Calendar/README.md": [
        "http://localhost:5001",
        "http://localhost:45005",
    ],
    "Control Center/README.md": [
        "http://localhost:8077",
        "http://localhost:45011",
    ],
    "Connect/README.md": [
        "http://localhost:5000",
        "http://localhost:45008",
    ],
    "Planet/README.md": [
        "http://localhost:46000",
        "http://localhost:45006",
    ],
    "Meet/README.md": [
        "45003",
        "6001",
    ],
    "Writer/README.md": [
        "http://localhost:45010",
        "http://localhost:6011",
        "./start.sh",
    ],
    "Learn/README.md": [
        "http://localhost:45009",
        "./start.sh",
    ],
    "Mail/README.md": [
        "http://localhost:8000",
        "http://localhost:45004",
    ],
    "Capital Hub/README.md": [
        "45013",
        "6033",
    ],
    "Secure/README.md": [
        "45012",
        "6004",
    ],
}


ACTIVE_SERVICE_READMES = [
    "Gate/README.md",
    "Atlas/README.md",
    "Calendar/README.md",
    "Control Center/README.md",
    "Connect/README.md",
    "Planet/README.md",
    "Meet/README.md",
    "Writer/README.md",
    "Learn/README.md",
    "Mail/README.md",
    "Capital Hub/README.md",
    "Secure/README.md",
]


REQUIRED_PREFLIGHT_COMMANDS = [
    "./runtime-matrix-gate.sh",
    "./contract-gate.sh",
]


def _empty_ports() -> Dict[str, Optional[int]]:
    return {"frontend": None, "backend": None}


def _parse_port_cell(value: str) -> Optional[int]:
    cleaned = value.strip()
    if not cleaned or cleaned == "-":
        return None
    match = re.search(r"\d+", cleaned)
    return int(match.group(0)) if match else None


def parse_ports_md(path: Path) -> Tuple[PortMap, PortMap]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    def parse_profile(header: str) -> PortMap:
        profile: PortMap = {}
        in_section = False
        for line in lines:
            if line.startswith("## "):
                in_section = line.strip() == header
                continue
            if not in_section:
                continue
            if not line.strip().startswith("|"):
                continue

            cols = [part.strip() for part in line.split("|")[1:-1]]
            if len(cols) < 3:
                continue
            if cols[0] in {"App / Service", "---"}:
                continue
            if cols[0].startswith("---"):
                continue

            key = PORTS_LABEL_TO_KEY.get(cols[0])
            if not key:
                continue
            profile[key] = {
                "frontend": _parse_port_cell(cols[1]),
                "backend": _parse_port_cell(cols[2]),
            }
        return profile

    profile_a = parse_profile("## Profile A: `start-all.sh` / service `start.sh`")
    profile_b = parse_profile("## Profile B: PM2 `ecosystem.config.cjs`")
    return profile_a, profile_b


def parse_start_all(path: Path) -> PortMap:
    text = path.read_text(encoding="utf-8")
    ports: PortMap = {}

    def normalize_service_key(name: str) -> Optional[str]:
        lower = name.lower()
        if "gate" in lower:
            return "gate"
        if "control center" in lower:
            return "control_center"
        if "calendar" in lower:
            return "calendar"
        if "atlas" in lower:
            return "atlas"
        if "planet" in lower:
            return "planet"
        if "meet" in lower:
            return "meet"
        if "font" in lower:
            return "fonts"
        if "writer" in lower:
            return "writer"
        if "secure" in lower:
            return "secure_frontend"
        if "capital hub" in lower:
            return "capital_hub_frontend"
        if "learn" in lower:
            return "learn_docs"
        if "connect" in lower:
            return "connect"
        return None

    for line in text.splitlines():
        match = re.match(r"#\s*\d+[a-z]?\.\s*(.+?)\s*[-\u2014]\s*Port\s*(.+)$", line.strip())
        if not match:
            continue

        service_name = match.group(1).strip()
        port_text = match.group(2).strip()
        key = normalize_service_key(service_name)
        if not key:
            continue

        current = ports.setdefault(key, _empty_ports())
        labelled_pairs = re.findall(r"(\d+)\s*\((frontend|backend)\)", port_text, flags=re.IGNORECASE)
        if labelled_pairs:
            for value, side in labelled_pairs:
                current[side.lower()] = int(value)
            continue

        numbers = [int(value) for value in re.findall(r"\d+", port_text)]
        if not numbers:
            continue
        if len(numbers) == 1:
            current["backend"] = numbers[0]
            continue

        # Default ordering in script comments is frontend/backend.
        current["frontend"] = numbers[0]
        current["backend"] = numbers[1]

    return ports


def _infer_default_port_from_source(path: Path) -> Optional[int]:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    patterns = [
        r"listeningPort\s*=\s*Number\(\s*process\.env\.[A-Z_]+\s*\|\|\s*(\d+)\s*\)",
        r"process\.env\.[A-Z_]+\s*\|\|\s*process\.env\.PORT\s*\|\|\s*(\d+)",
        r"process\.env\.PORT\s*\|\|\s*(\d+)",
        r"listeningPort:\s*process\.env\.[A-Z_]+\s*\|\|\s*(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None


def parse_pm2(root_dir: Path, config_path: Path) -> Tuple[PortMap, List[str]]:
    command = [
        "node",
        "-e",
        (
            f"const cfg=require('{config_path.as_posix()}'); "
            "console.log(JSON.stringify(cfg.apps||[]));"
        ),
    ]
    result = subprocess.run(
        command,
        cwd=root_dir,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    apps = json.loads(result.stdout)

    ports: PortMap = {}
    notes: List[str] = []
    for app in apps:
        name = app.get("name")
        target = PM2_APP_TO_TARGET.get(name)
        if not target:
            continue

        service_key, side = target
        current = ports.setdefault(service_key, _empty_ports())

        args = str(app.get("args") or "")
        explicit = re.search(r"--port\s+(\d+)", args)
        if explicit:
            current[side] = int(explicit.group(1))
            continue

        positional_http_server = re.search(r"http\.server\s+(\d+)", args)
        if positional_http_server:
            current[side] = int(positional_http_server.group(1))
            notes.append(
                f"{name}: inferred {side} port {current[side]} from http.server args"
            )
            continue

        source_rel = DEFAULT_PORT_SOURCE_BY_PM2_APP.get(name)
        inferred = _infer_default_port_from_source(root_dir / source_rel) if source_rel else None
        current[side] = inferred
        if source_rel:
            notes.append(
                f"{name}: inferred {side} port {inferred} from {source_rel}"
            )

    return ports, notes


def compare_ports(
    expected: PortMap,
    actual: PortMap,
    keys: List[str],
    profile_name: str,
) -> List[str]:
    failures: List[str] = []
    for key in keys:
        expected_entry = expected.get(key, _empty_ports())
        actual_entry = actual.get(key)
        if not actual_entry:
            failures.append(f"[{profile_name}] missing service mapping for '{key}'")
            continue

        for side in ("frontend", "backend"):
            expected_port = expected_entry.get(side)
            if expected_port is None:
                continue
            actual_port = actual_entry.get(side)
            if actual_port != expected_port:
                failures.append(
                    f"[{profile_name}] {key}.{side}: expected {expected_port}, got {actual_port}"
                )
    return failures


def validate_readme_runtime_contract(root_dir: Path) -> Tuple[int, int, List[str]]:
    failures: List[str] = []
    checked_tokens = 0

    for readme_path, expected_tokens in README_EXPECTATIONS.items():
        path = root_dir / readme_path
        if not path.exists():
            failures.append(f"[Docs] missing expected file '{readme_path}'")
            continue
        text = path.read_text(encoding="utf-8")
        for token in expected_tokens:
            checked_tokens += 1
            if token not in text:
                failures.append(
                    f"[Docs] {readme_path}: missing token '{token}'"
                )

    for readme_path in ACTIVE_SERVICE_READMES:
        path = root_dir / readme_path
        if not path.exists():
            failures.append(f"[Docs] missing expected file '{readme_path}'")
            continue
        text = path.read_text(encoding="utf-8")
        for command in REQUIRED_PREFLIGHT_COMMANDS:
            checked_tokens += 1
            if command not in text:
                failures.append(
                    f"[Docs] {readme_path}: missing pre-flight command '{command}'"
                )

    return len(README_EXPECTATIONS), checked_tokens, failures


def main() -> int:
    root_dir = Path(__file__).resolve().parents[1]
    ports_md = root_dir / "PORTS.md"
    start_all = root_dir / "start-all.sh"
    pm2_config = root_dir / "ecosystem.config.cjs"

    profile_a_expected, profile_b_expected = parse_ports_md(ports_md)
    profile_a_actual = parse_start_all(start_all)
    profile_b_actual, inference_notes = parse_pm2(root_dir, pm2_config)

    failures: List[str] = []
    failures.extend(compare_ports(profile_a_expected, profile_a_actual, PROFILE_A_CHECK_KEYS, "Profile A"))
    failures.extend(
        compare_ports(
            profile_b_expected,
            profile_b_actual,
            sorted(profile_b_expected.keys()),
            "Profile B",
        )
    )
    docs_files_checked, docs_tokens_checked, docs_failures = validate_readme_runtime_contract(root_dir)
    failures.extend(docs_failures)

    print("Runtime matrix validation summary:")
    print(f"- Profile A keys checked: {len(PROFILE_A_CHECK_KEYS)}")
    print(f"- Profile B keys checked: {len(profile_b_expected.keys())}")
    print(f"- README files checked: {docs_files_checked}")
    print(f"- README token checks: {docs_tokens_checked}")
    for note in inference_notes:
        print(f"  * {note}")

    if failures:
        print("\nRuntime matrix drift detected:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("\nRuntime matrix check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
