# EvidentiaAI — Medical Evidence Intelligence Platform

EvidentiaAI is an AI-powered medical evidence intelligence platform focused on enabling researchers, HEOR/RWE teams, Medical Affairs, and Evidence Synthesis professionals to discover, organize, validate and explore medical evidence.

Current development focus: Phase 0 (Foundation) and Phase 1 (Literature Discovery Agent).

Key components
- `services/pubmed_service.py`: PubMed integration using BioPython Entrez.
- `database/db.py`: SQLite helpers and schema (creates `data/evidentia.db`).
- `agents/literature_discovery_agent.py`: `LiteratureDiscoveryAgent` that searches PubMed and persists studies.
- `app.py` + `pages/`: Streamlit UI (Dashboard, Literature Discovery, Upload Center).

Requirements & environment
- Python 3.11 (CI uses 3.11)
- Create a `.env` from `.env.example` and set `PUBMED_EMAIL` before running PubMed searches.

Quickstart
1. Create and activate virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Copy `.env.example` → `.env` and set values:

```text
PUBMED_EMAIL=you@example.com
OPENAI_API_KEY=
NCBI_API_KEY=
```

4. Run tests:

```powershell
.venv\Scripts\python -m pytest -q
```

5. Launch Streamlit UI:

```powershell
.venv\Scripts\python -m streamlit run app.py
```

Notes
- DB path: `data/evidentia.db` (created automatically on first run).
- For PubMed: set `PUBMED_EMAIL` and optionally `NCBI_API_KEY` to respect NCBI policies.
- On Windows, installing `biopython` may require `numpy`; if pip builds numpy from source, consider installing a binary wheel first: `pip install numpy`.

Project structure
```
EvidentiaAI/
├── app.py
├── agents/
├── config/
├── database/
├── services/
├── pages/
├── data/
├── uploads/
├── logs/
├── tests/
├── requirements.txt
├── .env.example
└── README.md
```

Security
- Do not commit `.env` or database files. See `.gitignore`.

Roadmap & next steps
- Phase 2: Evidence Extraction Agent (design pending)
- Add `.env.example` (included) and CI improvements (linting, mypy, bandit)

