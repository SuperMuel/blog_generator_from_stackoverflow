# Layout inspired by :
# https://github.com/tonykipkemboi/trip_planner_agent/blob/main/streamlit_app.py


import streamlit as st
from crew.ai_models import AIModel
from crew.crew import generate_article


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
with st.sidebar:
    st.header("🔧 Paramètres")
    with st.form(key="settings"):
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
            disabled=True,  # Not supported yet
            height=100,
        )

        model = st.selectbox(
            "Choisissez le modèle d'IA :",
            options=AIModel.__members__.values(),
            index=0,
            format_func=lambda x: x.value,
        )

        submitted = st.form_submit_button(":sparkles: Générer")


if submitted:
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
                    existing_articles=None,
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
