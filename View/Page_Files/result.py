import streamlit as st
from PIL import Image

RESULT_INFO_MAP = {
        "fractured":
        {
            "name": "Törött csont",
            "description": "A képen törésre utaló jel látható. Ez csontsérülés jele lehet, javasolt szakorvos felkeresése.",
            "link": "https://www.hazipatika.com/betegsegek_a_z/csonttoresek"
        },
        "not_fractured":
        {
            "name": "Nem törött csont",
            "description": "Nem látható törés a képen. Ha a panaszok továbbra is fennállnak, javasolt szakorvosi vizsgálat.",
            "link": "https://www.hazipatika.com/betegsegek_a_z/csonttoresek"
        },
        "no_tumor":
        {
            "name": "Nincs daganat",
            "description": "Nem észlelhető daganatra utaló elváltozás a képen.",
            "link": "https://www.webbeteg.hu/cikkek/daganat/1241/agydaganat"
        },
        "glioma":
        {
            "name": "Glioma",
            "description": "A gliomák olyan típusú daganatok, amelyek a glia sejtekben kezdődnek a központi idegrendszerben. Fontos a pontos diagnózis és a szakorvosi konzultáció.",
            "link": "https://www.hazipatika.com/napi_egeszseg/daganatok/cikkek/sikerult_azonositani_a_leghalalosabb_agydaganatot"
        },
        "meningioma":
        {
            "name": "Meningioma",
            "description": "Az agyhártyadaganat, avagy meningeoma a kemény agyburok daganatos burjánzása, amely a csont és az agyállomány között képződik, és az esetek túlnyomó többségében jóindulatú.",
            "link": "https://www.hazipatika.com/betegsegek_a_z/agyhartyadaganat"
        },
        "pituitary":
        {
            "name": "Pituitary",
            "description": "Az agyalapi mirigy (hipofízis, hypophysis) borsónyi szerv a központi idegrendszerben, mely az endokrin rendszer fő szabályozó központja. A legtöbb daganatos elváltozása jóindulatú, a tünetek a tumor méretétől, sajátosságaitól, valamint az elhelyezkedésétől függően változóak lehetnek.",
            "link": "https://egeszsegvonal.gov.hu/a-a/2357-agyalapi-mirigy-daganata.html"
        },
        "other_tumor":
        {
            "name": "Nem alkalmas kép",
            "description": "A kép nem alkalmas arra hogy tumort detektáljunk rajta",
            "link": "https://www.webbeteg.hu/cikkek/daganat/1241/agydaganat"
        },
        "other_fracture":
        {
            "name": "Nem alkalmas kép",
            "description": "A kép nem alkalmas arra hogy csonttörést detektáljunk rajta",
            "link": "https://www.hazipatika.com/betegsegek_a_z/csonttoresek"
        }
    }

def result():
    """Kiiratja a predikcióhoz releváns eredményeket"""
    st.title("Eredmények")

    require_login()

    if "prediction" in st.session_state:

        st.subheader("MI Diagnózis:")
        st.write(f"**{RESULT_INFO_MAP[st.session_state['prediction']]['name']} osztályozás sikeres! (Konfidencia érték: {st.session_state['confidence'] * 100:.2f}%)**")
        st.warning(RESULT_INFO_MAP[st.session_state["prediction"]]['description'])

        if st.session_state["prediction"] == "other_tumor" or st.session_state["prediction"] == "other_fracture":
            st.write("Viszont az alábbi linken utána olvashat a témának.")
        else:
            st.write("Az alábbi linken utána olvashat specifikusan a témának.")
        st.write(RESULT_INFO_MAP[st.session_state["prediction"]]['link'])
        st.error("Ez az oldal nem helyettesíti az orvosi véleményt!")

        image = Image.open(st.session_state["file_path"])
        st.image(image, caption='Feltöltött kép')

        if "new_prediction_button" in st.session_state:
            del st.session_state["new_prediction_button"]

        if st.button("Új kép feltöltése"):
            st.switch_page("Page_Files/upload2.py")
    else:
        st.warning("Először tölts fel egy képet!")

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
result()


