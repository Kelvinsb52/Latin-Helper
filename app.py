import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.schema import SystemMessage
from langchain.prompts import SystemMessagePromptTemplate, ChatPromptTemplate, PromptTemplate
from langchain.schema import HumanMessage, AIMessage
from langchain.chains.question_answering import load_qa_chain



def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)  

    SYSTEM_PROMPT = """
    You are an expert Latin historian, translator, and teacher. Your role is to analyze and interpret Latin texts with precision.

    When the user provides a Latin poem:
    - Summarize it in Latin first.
    - Then provide an English translation of your summary.

    Additionally, whenever the user asks a question:
    - Present a well-known Latin proverb.
    - Explain its meaning, provide historical context, and translate it into English.
    - Ensure your explanations are engaging, informative, and historically accurate.

    Whenever you say something in Latin, make sure you always give a english translation
    Maintain a scholarly yet engaging tone in your responses.
    """

    condense_prompt = PromptTemplate(
        input_variables=["chat_history", "question"],
        template="""
        Given the following conversation history and a new question, rephrase it as a standalone question.

        Chat History:
        {chat_history}

        Follow-up Question:
        {question}

        Standalone Question:
        """
    )

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True  
    )

    conversational_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        condense_question_prompt=condense_prompt,
        chain_type="stuff",  
        memory=memory,  
        combine_docs_chain_kwargs={  
            "prompt": PromptTemplate(
                input_variables=["context", "question"],
                template=SYSTEM_PROMPT + "\n\nContext:\n{context}\n\nUser Question:\n{question}\n\nResponse:"
            )
        },
        verbose=True
    )

    return conversational_chain

def handle_userinput(user_question):
    if "conversation" not in st.session_state or st.session_state.conversation is None:
        st.warning("Please upload and process a PDF before asking questions.")
        return

    response = st.session_state.conversation({"question": user_question})

    chat_history = response.get("chat_history", [])

    st.session_state.chat_history = chat_history

    print("DEBUG: chat_history after processing:", chat_history)

    for message in chat_history:
        if isinstance(message, HumanMessage):  
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Time to learn Latin!", page_icon="🏛")

    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.markdown('<h1 class="stHeader">🏛 Time to Learn Latin!</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 18px; color: black;">Ask a question about your Latin poem:</p>', unsafe_allow_html=True)

    user_question = st.text_input("Type your question here...", key="latin_input")

    st.markdown('<style>div[data-baseweb="input"] { display: block !important; visibility: visible !important; }</style>', unsafe_allow_html=True)

    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click 'Process'", accept_multiple_files=True)

        if st.button("Process"):
            with st.spinner("Processing..."):
                if not pdf_docs:
                    st.error("Please upload at least one PDF before processing.")
                    return

                raw_text = get_pdf_text(pdf_docs)

                text_chunks = get_text_chunks(raw_text)

                vectorstore = get_vectorstore(text_chunks)

                st.session_state.conversation = get_conversation_chain(vectorstore)

                st.success("PDFs processed successfully! Start asking questions.")


if __name__ == '__main__':
    main()
