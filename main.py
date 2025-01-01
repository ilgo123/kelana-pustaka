import streamlit as st
from ui.pages import Pages

def main():
    st.set_page_config(
        page_title="Kelana Pustaka",
        page_icon="📚",
        layout="wide"
    )

    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = True

    if 'username' not in st.session_state:
        st.session_state.username = "ilgo"
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = ""
        
    if 'role' not in st.session_state:
        st.session_state.role = "admin"

    pages = Pages()
    
    if not st.session_state.logged_in:
        if st.session_state.current_page == "masuk":
            pages.render_login_page()
        if st.session_state.current_page == "regist":
            pages.render_register_page()
        if st.session_state.current_page == "":
            pages.render_public_page()
    else:
        pages.render_library_page()

if __name__ == "__main__":
    main()