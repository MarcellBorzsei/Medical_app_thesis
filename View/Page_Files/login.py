import streamlit as st
import requests

def login():
    """Bejelentkező oldal megjelenítése, ha be van jelentkezve a felhasználó és felhasználói akciók kezelése."""

    st.title("Bejelentkezés")

    if "logged_in_user" not in st.session_state:

        username = st.text_input("Felhasználónév")
        password = st.text_input("Jelszó", type="password")

        if st.button("Bejelentkezés"):
            response = requests.post("http://localhost:5000/auth/login", json={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                response_data = response.json()
                st.session_state["logged_in_user"] = response_data["username"]
                st.session_state["id"] = response_data["id"]
                st.success("Sikeres bejelentkezés " + st.session_state["logged_in_user"] + "!")
                st.rerun()
            else:
                st.error("Hibás felhasználónév vagy jelszó!")

        if st.button("Nincs még fiókod? Regisztrálj itt!"):
            st.switch_page("Page_Files/register.py")


def hide_login():
    """Bejelentkező oldal megjelenítése, ha a felhasználó be van jelentkezve."""
    if "logged_in_user" in st.session_state:
        st.info(f"Már be vagy jelentkezve, {st.session_state['logged_in_user']}! Kijelentkezéshez kattints az alábbi gombra.")

        # Logout button
        if st.button("Kijelentkezés"):
            del st.session_state["logged_in_user"]
            del st.session_state["id"]
            st.rerun()
        st.stop()

login()
hide_login()