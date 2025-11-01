from data.employees import generate_employee_data
import json
from dotenv import load_dotenv
import streamlit as st
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import logging
from assistant import Assistant
from prompt import SYSTEM_PROMPT, WELCOME_MESSAGE
from langchain_groq import ChatGroq
from gui import AssistantGUI


if __name__ == "__main__":

    # here is an example of how to use the get_user_data function
    # users = generate_employee_data(1)[0]
    # print("\n\n User Data:")
    # print(json.dumps(users, indent=4))

    load_dotenv()

    logging.basicConfig(level=logging.INFO)

    st.set_page_config(page_title="Umbrella Onboarding",
                       page_icon="☂", layout="wide")

    # loading employee data
    @st.cache_data(ttl=3600, show_spinner="Loading Employee Data...")
    def get_user_data():
        return generate_employee_data(1)[0]  # hashable object -> st.cache_data

    # loading vectorstore client
    @st.cache_resource(ttl=3600, show_spinner="Loading Vector Store...")
    def init_vectorstore(pdf_path):
        try:
            loader = PyPDFLoader(pdf_path)
            docs = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=2000, chunk_overlap=200)
            splits = text_splitter.split_documents(docs)

            embedding_provider = OpenAIEmbeddings()
            persistent_path = "./data/vectorstore"

            vectorstore = Chroma.from_documents(
                documents=splits,
                embedding=embedding_provider,
                persist_directory=persistent_path
            )
            return vectorstore  # mutable object -> st.cache_resource
        except Exception as e:
            st.error(f"Failed to initialize vector store: {str(e)}")
            return None

    customer_data = get_user_data()

    vectorstore = init_vectorstore("data/umbrella_corp_policies.pdf")

    llm_model = ChatGroq(model="llama-3.3-70b-versatile")

    if "customer" not in st.session_state:
        st.session_state.customer = customer_data
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "ai", "content": WELCOME_MESSAGE}]

    assistant = Assistant(
        system_prompt=SYSTEM_PROMPT,
        llm=llm_model,
        message_history=st.session_state.messages,
        employee_information=st.session_state.customer,
        vector_store=vectorstore
    )

    gui = AssistantGUI(assistant)
    gui.render()
