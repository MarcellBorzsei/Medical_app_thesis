import streamlit as st
import requests
import re

def is_valid_email(email):
    """Emailt regex alapján validál, majd visszadja hogy helyes-e a formátum"""
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)


def is_valid_age(age):
    """Életkort validál majd visszaadja hogy beleesik-e az intervallumba."""
    try:
        age = int(age)
        return 5 <= age <= 100
    except ValueError:
        return False


def is_valid_username(username):
    """Felhasználónév hosszát validálja, majd visszaadja hogy beleesik-e az intervallumba."""
    return 4 <= len(username) <= 30


def register():
    """Regisztrációs oldal megjelenítése, ha be van jelentkezve a felhasználó és felhasználói akciók kezelése."""

    st.title("Regisztráció")

    if "logged_in_user" not in st.session_state:

        username = st.text_input("Felhasználónév")
        email = st.text_input("Email")
        password = st.text_input("Jelszó", type="password")
        confirm_password = st.text_input("Jelszó megerősítése", type="password")
        age = st.text_input("Életkor")

        if st.button("Regisztráció"):
            if is_valid_username(username) and is_valid_email(email) and password == confirm_password and is_valid_age(age):
                response = requests.post("http://localhost:5000/register/register", json={
                    "username": username,
                    "email": email,
                    "password": password,
                    "age": age
                })

                if response.status_code == 200:
                    st.success("Sikeres regisztráció! Most már bejelentkezhetsz.")
                    if st.button("Bejelentkezés"):
                        st.switch_page("Page_Files/login.py")
                else:
                    st.error("Ezzel a felhasználónévvel vagy email címmel már regisztrálva van felhasználó.")
            else:
                if not is_valid_username(username):
                    st.warning("Felhasználónévnek 4-30 karakter hosszúnak kell lennie.")

                if email and not is_valid_email(email):
                    st.warning("Kérlek, adj meg egy érvényes email címet!")

                if password != confirm_password:
                    st.warning("A jelszavak nem egyeznek!")

                if age and not is_valid_age(age):
                    st.warning("Az életkor 5 és 100 év között kell legyen!")

def hide_register():
    """Regisztrációs oldal megjelenítése, ha a felhasználó be van jelentkezve."""
    if "logged_in_user" in st.session_state:
        st.info(f"Már be vagy jelentkezve, {st.session_state['logged_in_user']}! Kijelentkezéshez kattints az alábbi gombra.")

        if st.button("Kijelentkezés"):
            del st.session_state["logged_in_user"]
            del st.session_state["id"]
            st.rerun()

        st.stop()

register()
hide_register()
