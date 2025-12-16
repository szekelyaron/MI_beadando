import streamlit as st
import json
from pathlib import Path
from core.recommender import recommend_day_menu
from utils.feedback import update_feedback

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "foods.json"

if "rec" not in st.session_state:
    st.session_state.rec = {
        "menu": None,
        "score": None,
        "feedback_given": False,
        "feedback_message": None,
        "feedback_type": None
    }

@st.cache_data
def load_foods():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_foods(foods):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(foods, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Baby Menu AI", layout="centered")
st.title("Baba Étel Ajánló")

tabs = st.tabs(["Étel ajánlás", "Új étel felvitele"])

with tabs[0]:
    age = st.number_input("Baba életkora (hónap):", 4, 36, 8)
    selected_allergies = st.multiselect(
        "Allergiák:", ["tej", "tojás", "hal", "glutén", "szója"]
    )
    selected_textures = st.multiselect(
        "Kedvelt állagok:", ["püré", "puha", "darabos"], default=["püré"]
    )

    if st.button("Menü ajánlása"):
        foods = load_foods()
        if len(foods) >= 3:
            menu, score = recommend_day_menu(
                foods, age, selected_allergies, selected_textures
            )
            st.session_state.rec = {
                "menu": menu,
                "score": score,
                "feedback_given": False,
                "feedback_message": None,
                "feedback_type": None
            }
        else:
            st.session_state.rec = {
                "menu": None,
                "score": None,
                "feedback_given": False,
                "feedback_message": None,
                "feedback_type": None
            }

    rec = st.session_state.rec

    if rec["menu"]:
        st.subheader("Ajánlott napi menü:")
        for f in rec["menu"]:
            st.write(f"• {f['name']} ({f['texture']}, min. {f['min_age']} hó)")
        st.caption(f"Illeszkedés a megadott adatokhoz: {rec['score'] * 100:.1f}%")

        if not rec["feedback_given"]:
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Tetszett a menü"):
                    for f in rec["menu"]:
                        update_feedback(f["name"], True)
                    rec["feedback_given"] = True
                    rec["feedback_message"] = "Köszönjük a visszajelzést!"
                    rec["feedback_type"] = "success"
                    st.rerun()

            with col2:
                if st.button("Nem tetszett a menü"):
                    for f in rec["menu"]:
                        update_feedback(f["name"], False)
                    rec["feedback_given"] = True
                    rec["feedback_message"] = "Köszönjük a visszajelzést!"
                    rec["feedback_type"] = "warning"
                    st.rerun()

        if rec["feedback_message"]:
            if rec["feedback_type"] == "success":
                st.success(rec["feedback_message"])
            else:
                st.warning(rec["feedback_message"])

with tabs[1]:
    foods = load_foods()

    name = st.text_input("Étel neve:")
    min_age = st.number_input("Ajánlott életkor (hónap):", 4, 36, 6)
    texture = st.selectbox("Állag:", ["püré", "puha", "darabos"])
    allergens = st.multiselect(
        "Allergének:", ["tej", "tojás", "hal", "glutén", "szója"]
    )

    if st.button("Étel mentése"):
        if name.strip():
            foods.append({
                "name": name.strip(),
                "min_age": int(min_age),
                "texture": texture,
                "allergens": allergens
            })
            save_foods(foods)
            st.cache_data.clear()
            st.success("Az új étel sikeresen hozzáadva.")
