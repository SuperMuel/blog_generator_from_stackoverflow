# Layout inspired by :
# https://github.com/tonykipkemboi/trip_planner_agent/blob/main/streamlit_app.py


import streamlit as st
from crew import generate_article

st.set_page_config(
    page_icon="✏️",
    layout="wide",
)


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("✏️ Générateur d'articles")


st.subheader(
    "Les agents IA travaillent pour vous ✨",
    divider=True,
    anchor=False,
)
options = [
    "Français",
    "Anglais",
    "Espagnol",
    "Allemand",
]
with st.sidebar:
    st.header("🔧 Paramètres")
    with st.form(key="settings"):
        topic = st.text_input("Entrez le sujet de l'article :")
        language = st.selectbox(
            "Choisissez la langue :",
            options=[
                "Français",
                "Anglais",
                "Espagnol",
                "Allemand",
            ],
            index=0,
        )

        submitted = st.form_submit_button("Générer")


if submitted:
    with st.status(
        "🤖 **Agents au travail... Cela peut prendre quelques    minutes...**",
        state="running",
        expanded=True,
    ) as status:
        with st.container(height=500, border=False):
            try:
                result = generate_article(topic, language)
            except Exception as e:
                st.error(f"Une erreur est survenue {e}")
                status.update(label="❌ Une erreur est survenue !", state="error")
                result = None
        status.update(label="✅ Article rédigé !", state="complete", expanded=False)

    if result:
        st.subheader("Voilà votre article !", anchor=False, divider="rainbow")
        st.markdown(result)
