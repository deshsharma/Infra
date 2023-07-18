from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
import streamlit as st 
from streamlit_chat import message

def display_conversation(history):
    for i in range(len(history["generated"])):
        message(history["past"][i], is_user=True, key=str(i) + "_user")
        message(history["generated"][i], key=str(i))    

def main():
    st.title('Chat with 🐝')

    with st.expander("About the Chatbot"):
        st.markdown("""
            This is a Generative AI powered Chatbot that interacts with you and you can ask followup questions.
        """)

    persist_directory = "/app/db"
    model_directory = "/app/models"

    embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
    db = Chroma(persist_directory=persist_directory, embedding_function=embedding)
    retriever = db.as_retriever()
    
    local_llm = LlamaCpp(
        model_path="/app/ggml-vic13b-q5_1.bin",
        callback_manager=callback_manager,
        stop=["### Human:"],
        verbose=True,
        n_ctx=2048
    )
    chain = load_qa_chain(local_llm, chain_type="stuff")
    qa_chain = RetrievalQA.from_chain_type(
        llm=local_llm, 
        chain_type="stuff", 
        retriever=retriever, 
        return_source_documents=True
    )

    user_input = st.text_input("", key="input")
    if "generated" not in st.session_state:
        st.session_state["generated"] = ["I am ready to help you"]
    if "past" not in st.session_state:
        st.session_state["past"] = ["Hey there!"]
    if user_input:
        matching_docs = db.similarity_search(user_input, k=2)
        prompt_len = chain.prompt_length(docs=matching_docs, question=user_input)
        st.write(f"Prompt len: {prompt_len}")
        if prompt_len > local_llm.n_ctx:
            st.write(
                "Prompt length is more than n_ctx. This will likely fail. Increase model's context, reduce chunk's \
                sizes or question length, or retrieve fewer docs."
            )
        st.session_state["past"].append(user_input)
        response = chain.run(input_documents=matching_docs, question=user_input)
        st.write(response)
        st.session_state["generated"].append(response)

    if st.session_state["generated"]:
        display_conversation(st.session_state)

if __name__ == '__main__':
    main()
