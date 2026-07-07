import os
os.environ["HF_HUB_OFFLINE"] = "1"

from dotenv import load_dotenv
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

VECTORSTORE_PATH = "vectorstore"

def load_rag_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings
    )
    
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )
    
    llm = ChatGroq(
        model_name="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.5
    )
    
    prompt = PromptTemplate.from_template("""You are EduNova AI, an intelligent educational assistant.
Use the context below to answer the question clearly and concisely.
If you don't know the answer, say so honestly.
Do not add any extra text, tags, or follow-up questions.

Context: {context}

Question: {question}

Answer:""")
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def clean_output(text):
        if "Question:" in text:
            text = text.split("Question:")[0].strip()
        if "#educational_assistant" in text:
            text = text.split("#educational_assistant")[0].strip()
        return text.strip()
    
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
        | RunnableLambda(clean_output)
    )
    
    return chain, retriever
