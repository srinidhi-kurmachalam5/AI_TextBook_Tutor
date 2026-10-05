import ollama
import streamlit as st

st.title(":blue[*AI Textbook Tutor 👩🏻‍🏫*]")

with st.sidebar:
    st.header("Tutor Settings")

    levels = {
        "Beginner 🟢":
            "Explain the topic in very simple words using basic examples. "
            "Assume the student is a beginner. Give the answer in 3-4 lines.",

        "Intermediate 🟡":
            "Explain the topic clearly with important concepts and examples. "
            "Assume the student has basic knowledge. Give the answer in 5-6 lines.",

        "Advanced 🔴":
            "Explain the topic in detail using technical terms, examples and important points. "
            "Assume the student has good knowledge of the subject."
    }

    level = st.selectbox("Select difficulty level:", levels.keys())

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.success("Chat cleared!")

    uploaded_file = st.file_uploader("Upload your textbook!")

    context = ""
    
    if uploaded_file:
        st.success("File uploaded successfully!")

        with st.expander("Preview"):
            context = uploaded_file.read().decode("utf-8")
            st.text(context[:5000])


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


question = st.chat_input("Ask your textbook question...")

if question:

    with st.chat_message("user"):
        st.write(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    system_prompt = levels[level]

    if context:
        system_prompt += f"""
        Answer the question using the uploaded textbook/notes when possible.

        Textbook content:
        {context}
        """

    with st.spinner("Tutor is thinking..."):

        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                }
            ] + st.session_state.messages
        )

    answer = response["message"]["content"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.write(answer)