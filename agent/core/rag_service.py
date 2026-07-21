from core.llm_service import get_llm
from core.vector_store import search_documents
from core.prompts import ANSWER_PROMPT, GENERATE_QA_PROMPT

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        _llm = get_llm()
    return _llm


def build_context(documents):
    return "\n\n".join(
        f"Source: {doc.metadata}\nContent: {doc.page_content}"
        for doc in documents
    )


def get_sources(documents):
    sources = []

    for doc in documents:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page")

        if page is not None:
            sources.append(f"{source}, page {page + 1}")
        else:
            sources.append(source)

    return sorted(set(sources))


def answer_question(question):
    docs = search_documents(question)
    context = build_context(docs)

    prompt = ANSWER_PROMPT.format(
        question=question,
        context=context
    )

    response = _get_llm().invoke(prompt)

    return response.content, get_sources(docs)


def generate_qa(topic, difficulty, count):
    docs = search_documents(topic)
    context = build_context(docs)

    prompt = GENERATE_QA_PROMPT.format(
        topic=topic,
        difficulty=difficulty,
        count=count,
        context=context
    )

    response = _get_llm().invoke(prompt)

    return response.content, get_sources(docs)
