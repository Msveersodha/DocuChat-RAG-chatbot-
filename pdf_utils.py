import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter 
import os
from dotenv import load_dotenv
import streamlit as st
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_pinecone import PineconeVectorStore
import logging

load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_environment():
    """Load environment variables and return API keys."""
    load_dotenv()
    # PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    PINECONE_API_KEY = st.secrets["pinecone"]["pineconeapi_key"] 
    OPENAI_API_KEY = st.secrets["openai"]["openapi_key"]
    
    if not PINECONE_API_KEY or not OPENAI_API_KEY:
        raise ValueError("Missing API keys. Please set PINECONE_API_KEY and OPENAI_API_KEY.")
    return PINECONE_API_KEY, OPENAI_API_KEY


def initialize_pinecone(api_key, index_name="rag-index"):
    """Initialize Pinecone client and create index if it doesn't exist."""
    try:
        pc = Pinecone(api_key=api_key)
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=1536,
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1")
            )
            logger.info(f"Created index: {index_name}")
        else:
            logger.info(f"Index {index_name} already exists")
        return pc
    except Exception as e:
        logger.error(f"Error initializing Pinecone client: {str(e)}")
        raise


def initialize_embeddings(api_key):
    """Initialize OpenAI embeddings."""
    try:
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=api_key
        )
        return embeddings
    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        raise


def initialize_llm(api_key):
    """Initialize ChatOpenAI LLM."""
    try:
        llm = ChatOpenAI(
            model_name="gpt-4o-mini",
            openai_api_key=api_key,
            temperature=0.7
        )
        return llm
    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise


def store_chunks_in_pinecone(chunks, embedding_function, index_name="rag-index"):
    """Store text chunks in Pinecone vector store."""
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index = pc.Index(index_name)
        index.delete(delete_all=True)  # Clear existing vectors
        vector_store = PineconeVectorStore.from_texts(
            texts=chunks,
            embedding=embedding_function,
            index_name=index_name
        )
        logger.info(f"Stored {len(chunks)} chunks in Pinecone")
        return vector_store
    except Exception as e:
        logger.error(f"Error storing embeddings in Pinecone: {str(e)}")
        raise


def validate_pdf(file) -> tuple[bool, str, str]:
    try:

        file_content=file.read()

        doc = fitz.open(stream=file_content, filetype="pdf")
        page_count = len(doc)
        
        if page_count > 5:
            return False, f"PDF has {page_count} pages. Maximum allowed is 5.", ""

        full_text = ""
        for page in doc:
            full_text += page.get_text()

        word_count = len(full_text.split())

        if word_count > 10000:
            return False, f"PDF has {word_count} words. Maximum allowed is 10,000.", ""

        return True, "PDF is valid.", full_text
    
    except Exception as e:
        return False, f"Error reading PDF: {str(e)}", ""


def process_pdf_and_split(file, chunk_size=1000, chunk_overlap=200):
    try:


        file_content=file.read()
        # Step 1: Read PDF with PyMuPDF
        doc = fitz.open(stream=file_content, filetype="pdf")
        full_text = ""
        for page in doc:
            full_text += page.get_text()

        # Step 2: Split using LangChain's RecursiveCharacterTextSplitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", "!", "?", " ", ""],
        )

        chunks = splitter.split_text(full_text)
        return chunks
    except Exception as e:
        raise ValueError(f"Error processing PDF: {str(e)}")
