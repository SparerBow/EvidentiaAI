import streamlit as st
from agents.literature_discovery_agent import search_and_save
from database import db


def main():
    st.title('Literature Discovery')
    query = st.text_input('Enter search query', '')
    max_results = st.slider('Max results', 1, 100, 20)
    if st.button('Search') and query.strip():
        with st.spinner('Searching PubMed...'):
            studies = search_and_save(query, max_results=max_results)
        if studies:
            st.success(f'Retrieved and saved {len(studies)} studies')
        else:
            st.info('No studies found')

    st.markdown('---')
    st.header('Recent studies')
    rows = db.list_studies(50)
    for r in rows:
        st.markdown(f"**{r[2]}**  
PMID: {r[1]}  
Authors: {r[6]}  
Journal: {r[4]} ({r[5]})")
        with st.expander('Abstract'):
            st.write(r[3])


if __name__ == '__main__':
    main()
