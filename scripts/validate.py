#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "rules" / "services.json"
ALLOWED_PTM = {"statistics", "marketing", "external", "review", "functional"}
ALLOWED_WP = {None, "functional", "preferences", "statistics-anonymous", "statistics", "marketing"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    if not isinstance(data.get("schema_version"), int):
        fail("schema_version doit être un entier")
    if not data.get("catalog_version"):
        fail("catalog_version absent")
    services = data.get("services")
    if not isinstance(services, list) or not services:
        fail("services doit être une liste non vide")

    ids = set()
    for index, service in enumerate(services):
        sid = service.get("id", "")
        if not ID_RE.match(sid):
            fail(f"id invalide à l'index {index}: {sid!r}")
        if sid in ids:
            fail(f"id dupliqué: {sid}")
        ids.add(sid)
        if not service.get("label"):
            fail(f"label absent pour {sid}")
        if service.get("ptm_category") not in ALLOWED_PTM:
            fail(f"ptm_category invalide pour {sid}")
        if service.get("wp_consent_category") not in ALLOWED_WP:
            fail(f"wp_consent_category invalide pour {sid}")
        patterns = service.get("patterns")
        if not isinstance(patterns, list) or not all(isinstance(p, str) and p.strip() for p in patterns):
            fail(f"patterns invalides pour {sid}")

    print(f"OK: {len(services)} services, catalogue {data['catalog_version']}")


if __name__ == "__main__":
    main()
