import streamlit as st

from src.document_loader import (
    save_uploaded_files,
    load_documents,
    split_documents
)
from src.vector_store import add_documents_to_vector_store
from src.rag_service import answer_question, generate_qa


st.set_page_config(
    page_title="InterviewPilot Agent",
    layout="wide"
)

st.title("InterviewPilot Agent")
st.caption("Simple document-based Interview Q&A Agent using Groq + FAISS")

tab1, tab2, tab3 = st.tabs([
    "Upload Documents",
    "Ask Question",
    "Generate Q&A"
])


with tab1:
    st.subheader("Upload Documents")

    uploaded_files = st.file_uploader(
        "Upload PDF or TXT files",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if st.button("Index Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one document.")
        else:
            file_paths = save_uploaded_files(uploaded_files)
            documents = load_documents(file_paths)
            chunks = split_documents(documents)
            count = add_documents_to_vector_store(chunks)

            st.success(f"Indexed {count} chunks successfully.")


with tab2:
    st.subheader("Ask Question")

    question = st.text_input(
        "Enter your interview question",
        placeholder="Example: What is Microsoft Fabric Lakehouse?"
    )

    if st.button("Get Answer"):
        if not question:
            st.warning("Please enter a question.")
        else:
            answer, sources = answer_question(question)

            st.markdown(answer)

            if sources:
                st.subheader("Sources")
                for source in sources:
                    st.write(source)


with tab3:
    st.subheader("Generate Q&A")

    topic = st.text_input(
        "Enter topic",
        placeholder="Example: Azure Data Factory"
    )

    difficulty = st.selectbox(
        "Difficulty",
        ["Beginner", "Intermediate", "Advanced"]
    )

    count = st.number_input(
        "Number of Q&A",
        min_value=1,
        max_value=50,
        value=5
    )

    if st.button("Generate"):
        if not topic:
            st.warning("Please enter a topic.")
        else:
            result, sources = generate_qa(topic, difficulty, count)

            st.markdown(result)

            if sources:
                st.subheader("Sources")
                for source in sources:
                    st.write(source)