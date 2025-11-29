import sys
from pathlib import Path

import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]  
BACKEND_DIR = ROOT_DIR / "backend"

sys.path.append(str(BACKEND_DIR))

from search import search_kaufland  

st.set_page_config(page_title="Compară prețurile Kaufland", page_icon="🛒", layout="wide")

st.title("🛒 Căutare produse Kaufland (Glovo)")
st.write("Introdu un cuvânt (ex: *lapte*, *iaurt*, *ouă*) și apasă **Caută**.")


query = st.text_input("Produs de căutat", value="lapte")

if st.button("Caută"):

    if not query.strip():
        st.warning("Te rog introdu un cuvânt pentru căutare.")
    else:
        with st.spinner(f"Caut produse pentru „{query}”..."):
            try:
                results = search_kaufland(query)
            except Exception as e:
                st.error(f"A apărut o eroare la căutare: {e}")
                results = []

        if not results:
            st.info("Nu am găsit produse pentru acest cuvânt.")
        else:
            st.success(f"Am găsit {len(results)} produse:")

            cols_per_row = 3
            for i in range(0, len(results), cols_per_row):
                row_items = results[i:i + cols_per_row]
                cols = st.columns(len(row_items))

                for col, item in zip(cols, row_items):
                    name = item.get("name", "Fără nume")
                    price = item.get("price", None)
                    image = item.get("image", None)

                    with col:
                        if image:
                            st.image(image, use_container_width=True)
                        st.markdown(f"**{name}**")
                        if price is not None:
                            st.markdown(f"💰 **{price:.2f} RON**")
                        else:
                            st.markdown("💰 Preț indisponibil")
