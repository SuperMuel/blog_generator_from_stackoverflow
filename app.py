import time
import streamlit as st
from crew import generate_article

st.title("Article Generator")

topic = st.text_input("Enter the topic:")
language = st.selectbox(
    "Select the language:", options=["Français", "Anglais"], index=0
)

if st.button("Generate Article"):
    stopwatch_placeholder = st.empty()
    start_time = time.time()

    with st.spinner("Generating article..."):
        article = generate_article(topic, language)

    end_time = time.time()
    stopwatch_placeholder.text(
        f"Article generated in {end_time - start_time:.2f} seconds"
    )

    st.markdown(article)
