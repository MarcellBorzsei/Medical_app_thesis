import streamlit as st

def home():
    """Főoldal megjelenítése"""

    st.title("Üdvözöllek az alkalmazásban!")
    st.write("**Ez egy orvosi képdiagnosztikai alkalmazás. Jelentkezz be vagy regisztrálj az induláshoz!**")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Bejelentkezés"):
            st.switch_page("Page_Files/login.py")

    with col2:
        if st.button("Regisztráció"):
            st.switch_page("Page_Files/register.py")

home()