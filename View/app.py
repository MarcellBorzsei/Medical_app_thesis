import streamlit as st


pages = {
    "Kezdőlap": [
        st.Page("Page_Files/home.py", title="Kezdőlap"),
    ],
    "Profil": [
        st.Page("Page_Files/login.py", title="Bejelentkezés"),
        st.Page("Page_Files/register.py", title="Regisztráció"),
        st.Page("Page_Files/profile.py", title="Profil"),
    ],
    "Képfeltöltés": [
        st.Page("Page_Files/upload2.py", title="Feltöltés"),
        st.Page("Page_Files/result.py", title="Kiértékelés"),
    ],
}

pg = st.navigation(pages)
pg.run()