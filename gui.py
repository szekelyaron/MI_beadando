import streamlit as st
import json
from pathlib import Path
from core.recommender import recommend_day_menu
from utils.feedback import update_feedback

DATA_PATH = Path("data/foods.json")

def load_foods():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

st.set_page_config(page_title="Baby Menu AI", layout="centered")

st.title("Baby Menu AI – Baba Étel Ajánló")

st.header("Napi étel ajánlás")

age = st.number_input("Baba életkora (hónap):", min_value=4, max_value=36, value=8)

allergy_options = ["tej", "tojás", "hal", "glutén", "szója"]
selected_allergies = st.multiselect("Allergiák:", allergy_options)

texture_options = ["püré", "puha", "darabos"]
selected_textures = st.multiselect("Kedvelt állagok:", texture_options, default=["püré"])

if st.button("Menü ajánlása"):
    foods = load_foods()

    if len(foods) < 3:
        st.error("Nincs elég étel az ajánláshoz.")
    else:
        menu, score = recommend_day_menu(
            foods, age, selected_allergies, selected_textures
        )

        st.subheader("Ajánlott napi menü:")
        for f in menu:
            st.write(f"• {f['name']} ({f['texture']}, min. {f['min_age']} hó)")

        st.info(f"Menü pontszáma: {round(score, 2)}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Tetszett a menü"):
                for f in menu:
                    update_feedback(f["name"], True)
                st.success("Visszajelzés rögzítve.")

        with col2:
            if st.button("Nem tetszett a menü"):
                for f in menu:
                    update_feedback(f["name"], False)
                st.warning("Visszajelzés rögzítve.")
