import streamlit as st
import requests
from dicom2jpg import dicom2jpg
import tempfile
import os
from PIL import Image


def upload():
    """Képfeltöltő oldal megjelenítése, ha be van jelentkezve a felhasználó és felhasználói akciók kezelése."""
    st.title("Kép feltöltése")

    require_login()

    if "upload_choice" not in st.session_state:
        st.session_state["upload_choice"] = None

    if st.session_state["upload_choice"] is None:
        choice = st.radio(
            "Válaszd ki a feltöltési funkciót",
            ("Tumor klasszifikálás", "Csont megállapítása (Törött-e?)")
        )
        if st.button("Kiválasztás"):
            if choice == "Tumor klasszifikálás":
                st.session_state["upload_choice"] = "Tumor"
            elif choice == "Csont megállapítása (Törött-e?)":
                st.session_state["upload_choice"] = "Fracture"
            st.success(f"Funkció kiválasztva: {choice}")
            st.rerun()


    if st.session_state["upload_choice"] is not None:
        uploaded_file = st.file_uploader("Tölts fel egy MRI vagy röntgenképet, JPG vagy DICOM formátumban", type=["jpg", "dcm"])

        if st.button("Vissza a kategória választáshoz"):
            del st.session_state["upload_choice"]
            st.rerun()

        if uploaded_file is not None:
            if "file_key" not in st.session_state:
                st.session_state["file_key"] = ""

            try:
                if uploaded_file.name.endswith(".jpg"):
                    st.image(uploaded_file, caption="Feltöltött JPG kép", use_container_width=True)

                elif uploaded_file.name.endswith(".dcm"):
                    if st.session_state["file_key"] != uploaded_file.name:
                        files = {"file": uploaded_file}
                        response = requests.post("http://localhost:5000/convert/convert", files=files)

                        if response.status_code == 200:
                            prediction_data = response.json()
                            st.session_state["jpg_file_path"] = prediction_data['jpg_file_path']
                            st.session_state["file_key"] = uploaded_file.name
                        else:
                            st.error("Hiba a kép konvertálása közben.")

                    image = Image.open(st.session_state["jpg_file_path"])
                    st.image(image, caption='Feltöltött DICOM kép', use_container_width=True)

                else:
                    st.error("Nem támogatott kiterjesztésű kép. Kérlek tölts fel DICOM vagy JPG kiterjesztésű fájlt.")
            except Exception as e:
                st.error(f"Hiba történt a fájl feldolgozása közben: {e}")

            if st.button("Küldés elemzésre"):
                try:
                    if uploaded_file.name.endswith(".dcm"):
                        with open(st.session_state["jpg_file_path"], "rb") as f:
                            files = {"file": f.read()}
                    elif uploaded_file.name.endswith(".jpg"):
                        files = {"file": uploaded_file.getvalue()}
                    else:
                        files = {}
                        st.error("Nem támogatott kiterjesztésű kép. Kérlek tölts fel DICOM vagy JPG kiterjesztésű fájlt.")

                    data = {"id": st.session_state["id"]}
                    if st.session_state["upload_choice"] == "Tumor":
                        response = requests.post("http://localhost:5000/upload/upload_tumor", files=files, data=data)
                    elif st.session_state["upload_choice"] == "Fracture":
                        response = requests.post("http://localhost:5000/upload/upload_fracture", files=files, data=data)
                    else:
                        # Ebbe az ágba nem kerülhetünk
                        response = ""

                    if response.status_code == 200:
                        prediction_data = response.json()
                        st.session_state["new_prediction_button"] = True
                        st.session_state["prediction"] = prediction_data['prediction']
                        st.session_state["confidence"] = prediction_data['confidence']
                        st.session_state["file_path"] = prediction_data['file_path']
                        st.success("A predikció sikeres volt. Lépj a Kiértékelés oldalra, hogy lásd az eredményeket!")

                    else:
                        if st.session_state["upload_choice"] == "Tumor":
                            st.session_state["new_prediction_button"] = False
                            st.error("Hiba történt a tumor osztályozása során.")
                        elif st.session_state["upload_choice"] == "Fracture":
                            st.session_state["new_prediction_button"] = False
                            st.error("Hiba történt a törés osztályozása során.")
                except Exception as e:
                    st.error(f"Hiba a kép elküldése során: {e}")

    if "new_prediction_button" in st.session_state:
        if st.session_state["new_prediction_button"]:
            if st.button("Kiértékelés eredménye"):
                del st.session_state["new_prediction_button"]
                st.switch_page("Page_Files/result.py")

    if "new_prediction_button" in st.session_state :
        if st.button("Új kép kiértékelése"):
            st.session_state["upload_choice"] = None
            del st.session_state["new_prediction_button"]
            st.rerun()


def require_login():
    """Képfeltöltő oldal megjelenítése, ha a felhasználó nincs bejelentkezve, blokkolja a funkcionalitást."""
    if "logged_in_user" not in st.session_state:
        st.warning("Kérlek jelentkezz be a folytatáshoz!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Bejelentkezés"):
                st.switch_page("Page_Files/login.py")
        with col2:
            if st.button("Regisztráció"):
                st.switch_page("Page_Files/register.py")

        st.stop()
upload()
