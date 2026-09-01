#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / "rules" / "services.json"
SPIP_PLUGINS = ROOT / "rules" / "spip-plugins.json"
ALLOWED_PTM = {"statistics", "marketing", "external", "review", "functional"}
ALLOWED_WP = {None, "functional", "preferences", "statistics-anonymous", "statistics", "marketing"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
PREFIX_RE = re.compile(r"^[a-z0-9][a-z0-9_-]*$")


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main():
    data = json.loads(SERVICES.read_text(encoding="utf-8"))
    profiles = json.loads(SPIP_PLUGINS.read_text(encoding="utf-8"))
    if not isinstance(data.get("schema_version"), int):
        fail("schema_version services invalide")
    if not data.get("catalog_version"):
        fail("catalog_version services absent")
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
        if not service.get("privacy_kind"):
            fail(f"privacy_kind absent pour {sid}")
        if service.get("ptm_category") not in ALLOWED_PTM:
            fail(f"ptm_category invalide pour {sid}")
        if service.get("wp_consent_category") not in ALLOWED_WP:
            fail(f"wp_consent_category invalide pour {sid}")
        patterns = service.get("patterns")
        if not isinstance(patterns, list) or not all(isinstance(p, str) and p.strip() for p in patterns):
            fail(f"patterns invalides pour {sid}")
        prefixes = service.get("spip_plugin_prefixes", [])
        if not isinstance(prefixes, list) or not all(isinstance(p, str) and PREFIX_RE.match(p) for p in prefixes):
            fail(f"spip_plugin_prefixes invalides pour {sid}")

    plugins = profiles.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        fail("plugins SPIP doit être une liste non vide")
    prefixes = set()
    for plugin in plugins:
        prefix = plugin.get("prefix", "")
        if not PREFIX_RE.match(prefix):
            fail(f"préfixe SPIP invalide: {prefix!r}")
        if prefix in prefixes:
            fail(f"préfixe SPIP dupliqué: {prefix}")
        prefixes.add(prefix)
        if plugin.get("severity") not in {"info", "review", "high"}:
            fail(f"severity invalide pour {prefix}")
        if not plugin.get("privacy_kind"):
            fail(f"privacy_kind absent pour {prefix}")
        for sid in plugin.get("services", []):
            if sid not in ids:
                fail(f"service inconnu {sid} référencé par {prefix}")

    if data["catalog_version"] != profiles.get("catalog_version"):
        fail("versions catalogue services/SPIP différentes")

    print(f"OK: {len(services)} services, {len(plugins)} profils SPIP, catalogue {data['catalog_version']}")


if __name__ == "__main__":
    main()
