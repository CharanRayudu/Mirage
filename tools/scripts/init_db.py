"""
init_db.py — Initialize the findings.db SQLite database.

Creates two tables:
  - findings: canonical findings with evidence, severity, and reproduction steps.
  - evidence: individual evidence artifacts linked to findings.

Usage:
    python tools/scripts/init_db.py
"""
import sqlite3
import sys
import argparse
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DB_PATH = REPO_ROOT / "state" / "findings.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS vulnerabilities (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT    NOT NULL DEFAULT 'unknown',
    title           TEXT    NOT NULL,
    severity        TEXT    CHECK(severity IN ('critical','high','medium','low','info')) DEFAULT 'info',
    category        TEXT    DEFAULT '',
    owasp_category  TEXT    DEFAULT '',     -- A01-A10, API1-API10
    safety_level    TEXT    DEFAULT 'low',  -- low, medium, high
    description     TEXT    DEFAULT '',
    evidence_paths  TEXT    DEFAULT '[]',   -- JSON array of artifact paths
    reproduction    TEXT    DEFAULT '',     -- safe reproduction steps
    impact          TEXT    DEFAULT '',
    remediation     TEXT    DEFAULT '',
    status          TEXT    CHECK(status IN ('candidate','confirmed','false_positive','reported','VALIDATED')) DEFAULT 'candidate',
    confidence      REAL    DEFAULT 0.0,   -- 0.0 – 1.0
    node_id         TEXT    DEFAULT '',     -- attack_graph node that found this
    created_at      TEXT    DEFAULT (datetime('now')),
    updated_at      TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS evidence (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    vulnerability_id INTEGER NOT NULL REFERENCES vulnerabilities(id) ON DELETE CASCADE,
    artifact_path   TEXT    NOT NULL,
    description     TEXT    DEFAULT '',
    evidence_type   TEXT    CHECK(evidence_type IN ('har','screenshot','tool_output','log','code','other')) DEFAULT 'other',
    captured_at     TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS targets (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    domain          TEXT    NOT NULL UNIQUE,
    discovered_at   TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS endpoints (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT    NOT NULL,
    url             TEXT    NOT NULL UNIQUE,
    method          TEXT    DEFAULT 'GET',
    status_code     INTEGER DEFAULT 0,
    content_length  INTEGER DEFAULT 0,
    discovered_at   TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS parameters (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint_id     INTEGER REFERENCES endpoints(id) ON DELETE CASCADE,
    name            TEXT    NOT NULL,
    type            TEXT    DEFAULT 'string',
    discovered_at   TEXT    DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS tests (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id          TEXT    NOT NULL,
    tool            TEXT    NOT NULL,
    target_url      TEXT    NOT NULL,
    status          TEXT    DEFAULT 'completed',
    executed_at     TEXT    DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_evidence_vuln ON evidence(vulnerability_id);
CREATE INDEX IF NOT EXISTS idx_vuln_status  ON vulnerabilities(status);
CREATE INDEX IF NOT EXISTS idx_vuln_severity ON vulnerabilities(severity);
CREATE INDEX IF NOT EXISTS idx_endpoints_run_id ON endpoints(run_id);
"""


def init_db(db_path: Path) -> None:
    """Create (or update) the findings database."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()
    print(f"✓ Initialized findings database: {db_path.name} at {db_path.parent}")


def main():
    parser = argparse.ArgumentParser(description="Initialize Mirage findings database.")
    parser.add_argument("program", nargs="?", help="Name of the program to initialize DB for")
    args = parser.parse_args()

    if args.program:
        db_path = REPO_ROOT / "programs" / args.program / "findings.db"
    else:
        db_path = DEFAULT_DB_PATH
        
    init_db(db_path)

if __name__ == "__main__":
    main()
