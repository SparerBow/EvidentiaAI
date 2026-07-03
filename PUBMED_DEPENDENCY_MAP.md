# PubMed Dependency Map

This document shows external dependencies and NCBI/PubMed-specific elements used by the project.

Code locations:
- `services/pubmed_service.py` — BioPython Entrez usage: `Entrez.esearch`, `Entrez.efetch` (retmode=xml)
- `agents/literature_discovery_agent.py` — orchestrates search + fetch + DB persistence
- `database/db.py` — `insert_study`, `create_tables`, `insert_search_history`

External dependencies:
- Biopython (Entrez) — used to call NCBI e-utilities
- python-dotenv — for `.env` loading
- requests — (removed legacy usage) not required for PubMed code

Environment variables relevant to PubMed:
- `PUBMED_EMAIL` — required by Entrez as contact
- `NCBI_API_KEY` — optional; increases rate limits

NCBI rate-limiting guidance (implemented practices):
- Keep requests to <= 3 per second (we add pauses in client code where needed)
- Use `Entrez.api_key` when available

Notes
- Legacy file `services/pubmed_agent.py` removed; all PubMed logic lives in `services/pubmed_service.py` and the agent.
