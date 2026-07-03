import streamlit as st
from services.excel_service import save_upload, validate_excel


def main():
    st.title('Upload Center')
    uploaded = st.file_uploader('Upload Excel file', type=['xls', 'xlsx'])
    if uploaded:
        target = save_upload(uploaded, uploaded.name)
        ok, msg = validate_excel(target)
        if ok:
            st.success(f'Uploaded: {msg}')
        else:
            st.error(f'Validation failed: {msg}')


if __name__ == '__main__':
    main()
