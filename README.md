# EvdintiaAI — Literature Discovery

This project includes a Literature Discovery Agent that searches PubMed and saves study records to a local SQLite database.

**Key files**
- [services/pubmed_agent.py](services/pubmed_agent.py): PubMed ESearch/EFetch integration and DB saving.
- [database/db.py](database/db.py): SQLite helpers and `insert_study`/`list_studies` APIs.
- [scripts/run_pubmed_test.py](scripts/run_pubmed_test.py): Small runner to perform a search and save results.
- [scripts/verify_pubmed_import.py](scripts/verify_pubmed_import.py): Quick import sanity check (no network).

# EvdintiaAI — Literature Discovery

This project includes a Literature Discovery Agent that searches PubMed and saves study records to a local SQLite database.

**Key files**
- [services/pubmed_agent.py](services/pubmed_agent.py): PubMed ESearch/EFetch integration and DB saving.
- [database/db.py](database/db.py): SQLite helpers and `insert_study`/`list_studies` APIs.
- [scripts/run_pubmed_test.py](scripts/run_pubmed_test.py): Small runner to perform a search and save results.
- [scripts/verify_pubmed_import.py](scripts/verify_pubmed_import.py): Quick import sanity check (no network).

## NCBI API key and email

To increase rate limits and identify your tool to NCBI, set the following environment variables:

- `NCBI_API_KEY`: your NCBI e-utilities API key (optional but recommended).
- `NCBI_EMAIL`: your contact email (recommended by NCBI usage policies).

Example (PowerShell):

```
$env:NCBI_API_KEY = 'your_api_key_here'
$env:NCBI_EMAIL = 'you@example.com'
```

Example (bash/zsh):

```
export NCBI_API_KEY=your_api_key_here
export NCBI_EMAIL=your_email@example.com
```

The agent reads these variables automatically; you can also pass them directly to `search_and_save(query, max_results, api_key=..., email=...)`.

## Install and run

1. Create and activate a virtual environment (already present in this repo as `.venv` for development).
2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the smoke test (will create `data/evidence.db`):

```
python scripts/run_pubmed_test.py
```

4. Verify imports without network:

```
python scripts/verify_pubmed_import.py
```

## Database

The SQLite DB is stored at `data/evidence.db`. Use any SQLite client to inspect entries saved by the agent.

## Notes

- Respect NCBI rate limits: the agent includes a small sleep between inserts and supports API keys for higher limits.
- If running in environments without outbound network access, use `scripts/verify_pubmed_import.py` to confirm local setup.

## Next suggestions

- Add unit tests and CI to validate XML parsing and DB behavior.
- Add a CLI wrapper and configurable logging.
