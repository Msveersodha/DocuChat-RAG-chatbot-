import streamlit as st
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from pdf_utils import validate_pdf
from pdf_utils import process_pdf_and_split
from langchain.chains import RetrievalQA
from pdf_utils import load_environment, initialize_pinecone, initialize_embeddings, initialize_llm, store_chunks_in_pinecone
import logging

load_dotenv()
store=True

# Define API keys
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    PINECONE_API_KEY, OPENAI_API_KEY = load_environment()
except Exception as e:
    st.error(f"Error loading environment: {str(e)}")
    logger.error(f"Error loading environment: {str(e)}")
    st.stop()

# Initialize Pinecone
try:
    pc = initialize_pinecone(PINECONE_API_KEY)
    st.success("Pinecone client initialized successfully")
except Exception as e:
    st.error(f"Error initializing Pinecone: {str(e)}")
    st.stop()

# Initialize embeddings
try:
    embedding_function = initialize_embeddings(OPENAI_API_KEY)
except Exception as e:
    st.error(f"Error initializing embeddings: {str(e)}")
    st.stop()

# Initialize LLM
try:
    llm = initialize_llm(OPENAI_API_KEY)
except Exception as e:
    st.error(f"Error initializing LLM: {str(e)}")
    st.stop()


#------------------------------------- Streamlit Ui Design
Display=True
st.set_page_config(page_title="Your RAG Assistant", page_icon=":material/smart_toy:",layout="centered")

if Display:
    st.image("DcouChat_logo.jpg", width=150)
    st.title("AI-Powered Document Assistant")
    st.write("""
                **DocuChat** is a smart PDF-based assistant that allows you to upload a document and ask questions in natural language. It uses Retrieval-Augmented Generation (RAG) powered by LangChain, OpenAI, and Pinecone to provide accurate answers grounded in the document content. Whether it's resumes, reports, or study material, DocuChat helps you interact with complex PDFs in a conversational way.  
            ⚠️ *Note: Currently, DocuChat supports only one PDF at a time, with a limit of 5 pages or 10,000 words. Multi-document and long-format support are planned for future versions.*
            """)
    st.divider()
    
    file = st.file_uploader(
    "Upload Resume PDFs",
    type=["pdf"],
    accept_multiple_files=False
    )
    
    # Store PDF validation result
    if file and "pdf_validated" not in st.session_state:
        is_valid, msg, extracted_text = validate_pdf(file)
        st.session_state.pdf_validated = is_valid
        st.session_state.pdf_msg = msg
        st.session_state.pdf_text = extracted_text if is_valid else ""
        
    # Show validation result
    if file:
        # Reset file pointer after validation
        file.seek(0)
        if st.session_state.pdf_validated:
            st.success("✅ " + st.session_state.pdf_msg)
            chunks = process_pdf_and_split(file)
            # Store chunks in Pinecone
            if store:
                try:
                    vector_store = PineconeVectorStore.from_texts(
                    texts=chunks,
                    embedding=embedding_function,
                    index_name="rag-index",
                    )
                    st.success("✅ Successfully stored embeddings in Pinecone.")
                    store=False
                except Exception as e:
                    st.error(f"❌ Error storing embeddings in Pinecone: {str(e)}")
        else:
            st.error("❌ " + st.session_state.pdf_msg)
    
    if file and st.session_state.pdf_validated:
        question = st.text_area("Ask me! (Max 200 characters)", max_chars=200)

        if st.button("Submit", help="Click to get an answer"):
            if not question.strip():
                st.warning("Please enter a question.")
            else:
                with st.spinner("Thinking... Please wait ⏳"):
                    try:
                    # Initialize PineconeVectorStore
                        vector_store = PineconeVectorStore(
                            index_name="rag-index",
                            embedding=embedding_function
                        )
                        qa_chain = RetrievalQA.from_chain_type(
                            llm=llm,
                            chain_type="stuff",
                            retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
                        )
                    # Perform similarity search
                        answer = qa_chain.run(question)
                        st.subheader("Answer:")
                        st.write(answer)
                        st.divider()
                    except Exception as e:
                        st.error(f"❌ Error retrieving data from Pinecone: {str(e)}")
                    
    else:
        st.info("Upload a valid PDF to ask questions.")
