# Phase 2 Migration Plan (High level)

This document outlines a migration and preparation plan for Phase 2 (Evidence Extraction Agent) and for moving from SQLite to PostgreSQL in the future.

1. Database migration strategy
   - Keep current SQLite schema as source of truth for MVP.
   - Introduce SQLAlchemy ORM layer and Alembic for migrations.
   - Create mapping of current tables (`studies`, `search_history`) to ORM models.
   - Use a migration script to generate PostgreSQL schema from ORM models.

2. Backups and data mobility
   - Implement export tool to dump SQLite rows to CSV/JSON.
   - Provide `scripts/import_to_pg.py` to import CSV into Postgres.

3. Versioning and rollout
   - Add integration tests verifying parity between SQLite and Postgres imports.
   - Roll out Postgres feature flag for read/write in staging before production.

4. Evidence atom model
   - Design `evidence_atoms` table with normalized fields and references to `studies`.
   - Provide migration.md with mapping from study fields to atoms.

5. Timeline (example)
   - Week 1: Add SQLAlchemy models and Alembic setup
   - Week 2: Implement import/export tools and tests
   - Week 3: Staging Postgres deployment and data import
