import streamlit as st
from database import db


def main():
    st.title('EvidentiaAI — Dashboard')

    total = len(db.list_studies(100000))
    st.metric('Total Studies', total)

    st.header('Latest Searches')
    searches = db.list_search_history(10)
    if searches:
        for s in searches:
            st.write(f"{s[2]} — {s[1]}")
    else:
        st.write('No searches yet')

    st.header('Database Health')
    st.write('DB file: data/evidentia.db')


if __name__ == '__main__':
    main()
