import streamlit as st
import requests
from PIL import Image
import os

def fetch_user_data():
    """Profil oldal megjelenítéséhez szükséges adatok lekérése."""
    if "logged_in_user" not in st.session_state:
        st.error("Először jelentkezz be a profilod megtekintéséhez!")
        st.stop()

    personal_data_response = requests.get(f"http://localhost:5000/profile/personal_data?username={st.session_state['logged_in_user']}")
    if personal_data_response.status_code == 200:
        personal_data = personal_data_response.json()
    else:
        st.error("Nem sikerült lekérni a felhasználói adatokat.")
        return None, None

    images_response = requests.get(f"http://localhost:5000/profile/pictures?id={st.session_state['id']}")
    if images_response.status_code == 200:
        uploaded_images = images_response.json()
    else:
        st.error("Nem sikerült lekérni a felhasználó által feltöltött képeket.")
        return None, None

    return personal_data, uploaded_images

def profile():
    """Profil oldal megjelenítése, ha be van jelentkezve a felhasználó és felhasználói akciók kezelése."""
    st.title("Profilom")

    user_data, uploaded_images = fetch_user_data()

    if user_data:
        st.subheader("Felhasználói adatok")
        st.write(f"**Felhasználónév:** {user_data['username']}")
        st.write(f"**Email:** {user_data['email']}")
        st.write(f"**Életkor:** {user_data['age']}")

    if uploaded_images:
        st.subheader("Feltöltött képek és diagnózisok")
        col1, col2 = st.columns(2)

        for i, uploaded_image in enumerate(uploaded_images):
            image_path = uploaded_image["image_url"]
            predicted_label = uploaded_image["predicted_label"]

            if os.path.exists(image_path):
                image = Image.open(image_path)
                with (col1 if i % 2 == 0 else col2):
                    st.image(image, caption=f"Predikció: {predicted_label}", use_container_width=True)

    else:
        st.info("Még nem töltöttél fel képeket.")

profile()