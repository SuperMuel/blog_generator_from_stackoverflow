# Layout inspired by :
# https://github.com/tonykipkemboi/trip_planner_agent/blob/main/streamlit_app.py

import streamlit as st
from crew.ai_models import AIModel
from crew.crew import generate_article
import pandas as pd
import lorem

from st_copy_to_clipboard import st_copy_to_clipboard


def mock_article(
    title: str = "Article", nb_paragraphs: int = 5, nb_subsections: int = 3
) -> str:
    if not title:
        title = "Article"
    result = f"# {title}"
    for i in range(nb_paragraphs):
        result += "\n\n" + f"## Paragraphe {i+1}"
        for j in range(nb_subsections):
            result += "\n\n" + f"### Sous-section {chr(65 + j)}"
            p = lorem.paragraph()
            result += "\n\n" + p

    return result


if "existing_articles" not in st.session_state:
    # create empty dataframe with "title", "url" and "summary" columns
    df = pd.DataFrame(columns=["title", "url", "summary"])
    st.session_state["existing_articles"] = df


# From https://github.com/tonykipkemboi/trip_planner_agent/blob/main/trip_agents.py
def streamlit_callback(step_output):
    st.markdown("---")
    for step in step_output:
        if isinstance(step, tuple) and len(step) == 2:
            action, observation = step
            if (
                isinstance(action, dict)
                and "tool" in action
                and "tool_input" in action
                and "log" in action
            ):
                st.markdown("# Action")
                st.markdown(f"**Tool:** {action['tool']}")
                st.markdown(f"**Tool Input** {action['tool_input']}")
                st.markdown(f"**Log:** {action['log']}")
                st.markdown(f"**Action:** {action['Action']}")
                st.markdown(f"**Action Input:** ```json\n{action['tool_input']}\n```")
            elif isinstance(action, str):
                st.markdown(f"**Action:** {action}")
            else:
                st.markdown(f"**Action:** {str(action)}")

            st.markdown("**Observation**")
            if isinstance(observation, str):
                observation_lines = observation.split("\n")
                for line in observation_lines:
                    if line.startswith("Title: "):
                        st.markdown(f"**Title:** {line[7:]}")
                    elif line.startswith("Link: "):
                        st.markdown(f"**Link:** {line[6:]}")
                    elif line.startswith("Snippet: "):
                        st.markdown(f"**Snippet:** {line[9:]}")
                    elif line.startswith("Question title: "):
                        st.markdown(f"**Question title:** {line[16:]}")
                    elif line.startswith("Question link: "):
                        st.markdown(f"**Question link:** {line[15:]}")
                    elif line.startswith("Best answer URL: "):
                        st.markdown(f"**Best answer URL:** {line[17:]}")
                    elif line.startswith("-"):
                        st.markdown(line)
                    else:
                        st.markdown(line)
            else:
                st.markdown(str(observation))
        else:
            st.markdown(step)


st.set_page_config(
    page_icon="✏️",
    layout="wide",
    page_title="Générateur d'articles",
    menu_items={"Report a bug": "mailto:samuel@timtek.fr"},
)


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


icon("✏️ Générateur d'articles")


@st.experimental_dialog(  # type: ignore
    "Vos anciens articles", width="large"
)
def show_existing_articles():
    st.info(
        "Les agents analyseront ces articles afin de les lier à votre nouveau contenu.",
        icon="ℹ️",
    )

    config = {
        "title": st.column_config.TextColumn(
            "Titre",
            width="large",
            required=True,
        ),
        "url": st.column_config.TextColumn(
            "Url",
            required=True,
            max_chars=500,
            width="small",
        ),
        "summary": st.column_config.TextColumn(
            "Résumé",
            required=False,
            max_chars=10000,
        ),
    }

    initial_df = st.session_state["existing_articles"].copy()

    edited_df = st.data_editor(
        initial_df,
        num_rows="dynamic",
        column_config=config,
        hide_index=True,
    )

    st.caption(
        "Note : Vous pouvez copier-coller des lignes depuis un tableur pour les ajouter ici."
    )

    # TODO : check if modified

    if st.button("💾 Sauvegarder les modifications"):
        st.session_state["existing_articles"] = edited_df
        st.success("Modifications sauvegardées !")
        st.rerun()

    if st.button("❌ Annuler"):
        st.rerun()


st.subheader(
    "Les agents IA travaillent pour vous ✨",
    divider=True,
    anchor=False,
)
with st.sidebar:
    topic = st.text_input(
        "Entrez le sujet de l'article :",
        placeholder="Rust vs Python en 2024",
    )
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
    context = st.text_area(
        "Contexte (optionnel) :",
        placeholder="Example.com est une entreprise aux services du numérique implantée dans Lyon.",
        height=100,
    )

    checkbox_col, dialog_col = st.columns(2)

    with checkbox_col:
        make_internal_links = st.checkbox(
            " 🔗 Maillage Interne",
            help="Insérer des liens vers vos anciens articles pour améliorer le SEO ?",
            value=True,
        )

    with dialog_col:
        if st.button(
            f"📚 Vos anciens articles ({len(st.session_state.existing_articles)})"
        ):
            show_existing_articles()

    model = st.selectbox(
        "Choisissez le modèle d'IA :",
        options=AIModel.__members__.values(),
        index=0,
        format_func=lambda x: x.value,
    )

    submitted = st.button(":sparkles: Générer")  # TODO : disable if already generating


def get_selected_articles() -> list[dict] | None:
    if not make_internal_links:
        print("Linkage disabled")
        return None

    # show number of articles
    print(f"Number of articles selected : {len(st.session_state['existing_articles'])}")

    articles = st.session_state["existing_articles"].to_dict(orient="records")
    assert isinstance(articles, list)
    assert all("title" in article for article in articles)
    assert all("url" in article for article in articles)

    return articles


if submitted:
    if not model:
        st.error("Veuillez choisir un modèle d'IA.")
        st.stop()

    with st.status(
        "🤖 **Agents au travail... Cela peut prendre quelques    minutes...**",
        state="running",
        expanded=True,
    ) as status:
        with st.container(height=500, border=False):
            try:
                result = generate_article(
                    llm=model.to_client(),
                    topic=topic,
                    language=language,
                    context=context,
                    existing_articles=get_selected_articles(),
                    global_step_callback=streamlit_callback,
                )
                status.update(
                    label="Article rédigé !", state="complete", expanded=False
                )
            except Exception as e:
                st.error(e)
                status.update(label="Une erreur est survenue !", state="error")
                result = None

    if result:
        st.markdown(result)
        st_copy_to_clipboard(
            result,
            before_copy_label="📋 Copier l'article généré",
            after_copy_label="✅ Texte copié !",
        )

else:  # if not submitted
    st.markdown(
        """
        ## 📝 Instructions
        1. Entrez le sujet de l'article.
        2. Choisissez la langue.
        3. (Optionnel) Ajoutez un contexte afin que les agents comprennent mieux votre besoin.
        4. (Optionnel) Cochez la case pour activer le maillage interne, et sélectionnez vos anciens articles pour améliorer le SEO.
        5. Cliquez sur **:sparkles: Générer**.
        """
    )
