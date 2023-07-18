from langchain.llms import LlamaCpp
from langchain import PromptTemplate, LLMChain
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
n_gpu_layers = 40  
n_batch = 1024 
template = "testing template for {input} and {output}"
template = """
Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:
"""
prompt = PromptTemplate(input_variables=['query', 'conversation'], template=template)
prompt.format(query='desh', conversation='sharma')
callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])
llm = LlamaCpp(model_path="/app/ggml-vic13b-q5_1.bin",n_batch=n_batch,callback_manager=callback_manager, verbose=True,)
llm_chain = LLMChain(prompt=prompt, llm=llm)
llm_chain.run(query='desh', conversation='sharma')