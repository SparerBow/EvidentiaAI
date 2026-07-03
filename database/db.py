import sqlite3
import os

os.makedirs("data", exist_ok=True)

DB_NAME = "data/evidence.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS studies (
        study_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pmid TEXT UNIQUE,
        title TEXT,
        abstract TEXT,
        journal TEXT,
        publication_year TEXT,
        authors TEXT,
        source TEXT,
        relevance_score REAL
    )
    """)

    conn.commit()
    conn.close()


def insert_study(study: dict):
    """Insert or update a study record.

    study keys: pmid, title, abstract, journal, publication_year, authors, source, relevance_score
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """
            INSERT INTO studies (pmid, title, abstract, journal, publication_year, authors, source, relevance_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                study.get("pmid"),
                study.get("title"),
                study.get("abstract"),
                study.get("journal"),
                study.get("publication_year"),
                study.get("authors"),
                study.get("source"),
                study.get("relevance_score"),
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        # record exists, perform an update
        cur.execute(
            """
            UPDATE studies
            SET title = ?, abstract = ?, journal = ?, publication_year = ?, authors = ?, source = ?, relevance_score = ?
            WHERE pmid = ?
            """,
            (
                study.get("title"),
                study.get("abstract"),
                study.get("journal"),
                study.get("publication_year"),
                study.get("authors"),
                study.get("source"),
                study.get("relevance_score"),
                study.get("pmid"),
            ),
        )
        conn.commit()
    finally:
        conn.close()


def get_study_by_pmid(pmid: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM studies WHERE pmid = ?", (pmid,))
    row = cur.fetchone()
    conn.close()
    return row


def list_studies(limit: int = 100):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM studies ORDER BY study_id DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    create_tables()
    print("Database created successfully.")