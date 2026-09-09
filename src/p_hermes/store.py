"""SQLite persistence for workflow, knowledge and audit events.

State and its receipt share one transaction. This is a local single-user trust
boundary, not authentication or a remote authorization service.
"""
from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
import sqlite3

from .core import ContractError, canonical, digest, identifier, require_text


class Store:
    def __init__(self, path: str | Path):
        self.db = sqlite3.connect(path, isolation_level=None, timeout=10)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            PRAGMA foreign_keys=ON;
            CREATE TABLE IF NOT EXISTS jobs (
              id TEXT PRIMARY KEY, revision INTEGER NOT NULL, state TEXT NOT NULL,
              plan TEXT NOT NULL, plan_digest TEXT NOT NULL, approved_digest TEXT);
            CREATE TABLE IF NOT EXISTS events (
              sequence INTEGER PRIMARY KEY, job_id TEXT NOT NULL REFERENCES jobs(id),
              revision INTEGER NOT NULL, action TEXT NOT NULL, details TEXT NOT NULL,
              created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),
              UNIQUE(job_id,revision));
            CREATE TABLE IF NOT EXISTS knowledge (
              id TEXT PRIMARY KEY, title TEXT NOT NULL, body TEXT NOT NULL,
              source_ref TEXT NOT NULL, license_ref TEXT NOT NULL,
              state TEXT NOT NULL CHECK(state IN ('active','retired')));
        """)

    def close(self):
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            self.db.execute("ROLLBACK")
            raise
        else:
            self.db.execute("COMMIT")

    def job(self, job_id: str) -> dict:
        row = self.db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
        if row is None:
            raise ContractError("unknown job")
        value = dict(row)
        value["plan"] = json.loads(value["plan"])
        return value

    def _event(self, job_id, revision, action, details):
        self.db.execute("INSERT INTO events(job_id,revision,action,details) VALUES(?,?,?,?)",
                        (job_id, revision, action, canonical(details)))

    def create_job(self, job_id: str, plan: dict) -> dict:
        identifier(job_id)
        self._validate_plan(plan)
        try:
            with self.transaction():
                self.db.execute("INSERT INTO jobs VALUES(?,0,'draft',?,?,NULL)",
                                (job_id, canonical(plan), digest(plan)))
                self._event(job_id, 0, "create", {"plan_digest": digest(plan)})
        except sqlite3.IntegrityError as exc:
            raise ContractError("duplicate job") from exc
        return self.job(job_id)

    @staticmethod
    def _validate_plan(plan):
        if not isinstance(plan, dict):
            raise ContractError("plan must be an object")
        require_text(plan.get("purpose"), "plan purpose")
        canonical(plan)

    def act(self, job_id: str, revision: int, action: str, *, plan=None,
            approved_digest=None, evidence=None) -> dict:
        """CAS mutation. Unknown outcomes require reconciliation before completion.

        'approve' records a caller-supplied decision, not proof of user identity.
        A changed draft plan always clears approval. No automatic retry occurs.
        """
        if type(revision) is not int or revision < 0:
            raise ContractError("revision must be a nonnegative integer")
        with self.transaction():
            current = self.job(job_id)
            if current["revision"] != revision:
                raise ContractError("stale revision; reload before deciding")
            state = current["state"]
            details = {}
            if action == "revise" and state in {"draft", "approved"}:
                self._validate_plan(plan)
                current.update(plan=plan, plan_digest=digest(plan), approved_digest=None, state="draft")
                details = {"plan_digest": current["plan_digest"]}
            elif action == "approve" and state == "draft":
                if approved_digest != current["plan_digest"]:
                    raise ContractError("approval must bind the exact current plan digest")
                current.update(approved_digest=approved_digest, state="approved")
                details = {"approved_digest": approved_digest}
            elif action == "start" and state == "approved":
                if current["approved_digest"] != current["plan_digest"]:
                    raise ContractError("plan approval is stale")
                current["state"] = "running"
            elif action in {"complete", "fail", "unknown"} and state == "running":
                require_text(evidence, "observed evidence")
                current["state"] = {"complete": "completed", "fail": "failed", "unknown": "unknown"}[action]
                details = {"evidence": evidence}
            elif action in {"reconcile_complete", "reconcile_fail"} and state == "unknown":
                require_text(evidence, "reconciliation evidence")
                current["state"] = "completed" if action == "reconcile_complete" else "failed"
                details = {"evidence": evidence}
            else:
                raise ContractError(f"action {action!r} is invalid from {state!r}")
            self.db.execute("UPDATE jobs SET revision=?,state=?,plan=?,plan_digest=?,approved_digest=? WHERE id=?",
                            (revision + 1, current["state"], canonical(current["plan"]),
                             current["plan_digest"], current["approved_digest"], job_id))
            self._event(job_id, revision + 1, action, details)
        return self.job(job_id)

    def events(self, job_id: str) -> list[dict]:
        rows = self.db.execute("SELECT * FROM events WHERE job_id=? ORDER BY sequence", (job_id,))
        return [dict(row) | {"details": json.loads(row["details"])} for row in rows]

    def register_knowledge(self, item: dict):
        if not isinstance(item, dict):
            raise ContractError("knowledge must be an object")
        identifier(item.get("id"))
        for key in ("title", "body", "source_ref", "license_ref"):
            require_text(item.get(key), key)
        # Eligibility is explicitly declared, never inferred from missing fields.
        if item.get("public") is not True:
            raise ContractError("knowledge must be explicitly marked public")
        try:
            self.db.execute("INSERT INTO knowledge VALUES(?,?,?,?,?,'active')",
                            tuple(item[k] for k in ("id", "title", "body", "source_ref", "license_ref")))
        except sqlite3.IntegrityError as exc:
            raise ContractError("duplicate knowledge identifier") from exc

    def retire_knowledge(self, knowledge_id: str):
        cursor = self.db.execute("UPDATE knowledge SET state='retired' WHERE id=?", (knowledge_id,))
        if cursor.rowcount != 1:
            raise ContractError("unknown knowledge identifier")

    def search(self, query: str) -> list[dict]:
        """Literal case-insensitive substring retrieval, not semantic ranking."""
        require_text(query, "query")
        rows = self.db.execute("SELECT * FROM knowledge WHERE state='active' ORDER BY id")
        needle = query.casefold()
        return [dict(row) for row in rows if needle in (row["title"] + " " + row["body"]).casefold()]
