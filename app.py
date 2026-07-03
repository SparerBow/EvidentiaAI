import streamlit as st
from agents.literature_discovery_agent import search_and_save
from database import db
from config.logger import get_logger

logger = get_logger(__name__)


def main():
    st.title('EvidentiaAI — Literature Discovery')
    st.write('Enter a medical search query to retrieve PubMed studies.')

    query = st.text_input('Search query', value='')
    max_results = st.number_input('Max results', min_value=1, max_value=100, value=20)
    if st.button('Search') and query.strip():
        with st.spinner('Searching PubMed...'):
            studies = search_and_save(query, max_results=max_results)
        if studies:
            st.success(f'Retrieved and saved {len(studies)} studies')
        else:
            st.info('No studies found or an error occurred.')

    st.header('Recent Studies')
    rows = db.list_studies(50)
    for r in rows:
        st.subheader(f"{r[2]} ({r[6]})")
        st.write(f"PMID: {r[1]} — {r[4]} — {r[5]}")
        st.write(r[3])


if __name__ == '__main__':
    main()
