# from load_data import load_docs, split_docs, embed_load_docs
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.vectorstores import Chroma
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import RetrievalQA
import sys



persist_directory = "/app/db"
model_directory = "/app/models"

embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

def get_matching_documents( ,k=3,score=False):
  if score:
    similar_docs = vectordb.similarity_search_with_score(query,k=k)
  else:
    similar_docs = vectordb.similarity_search(query,k=k)
  return similar_docs

local_llm = LlamaCpp(
         model_path="/app/ggml-vic13b-q5_1.bin",
         stop=["### Human:"],
         callback_manager=callback_manager,
         verbose=True,
         n_ctx=2048,
         n_batch=512,
     )
chain = load_qa_chain(local_llm, chain_type="stuff")
def get_answer(query):
    similar_docs = get_matching_documents(query)
    answer = chain.run(input_documents=similar_docs, question=query)
    return answer
get_answer(query)


retriever = vectordb.as_retriever(search_kwargs={"k": 3})
#local_llm = LlamaCpp(model_path="../models/ggml-vic13b-q5_1.bin",verbose=True, n_ctx=2048)

local_llm = LlamaCpp(
        model_path="/app/models/ggml-vic13b-q5_1.bin",
        callback_manager=callback_manager,
        stop=["### Human:"],
        verbose=True,
        n_ctx=2048,
        n_batch=512,
    )
chain = load_qa_chain(local_llm, chain_type="stuff")
def get_anwer(query):
    smilar_docs = get_smil
if "Helpful Answer:" in chain.llm_chain.prompt.template:
        chain.llm_chain.prompt.template = (
            f"### Human:{chain.llm_chain.prompt.template}".replace(
                "Helpful Answer:", "\n### Assistant:"
            )
        )

qa_chain = RetrievalQA.from_chain_type(llm=local_llm, 
                                  chain_type="stuff", 
                                  retriever=retriever, 
                                  return_source_documents=True)

llm_response = qa_chain("How to make coffee?")
for key, value in llm_response.items():
    print(key +" =================================\n")
    print(value)
    print("=================================\n")
response_type = type(llm_response)
print("*******************\n")
part_before_human = llm_response['result'].split('\n### Human:')[0]
print(part_before_human)
print("******************\n")

# llm_response = qa_chain("How to make?")
print(llm_response)