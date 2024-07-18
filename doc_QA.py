from functools import cache
import sys
import os
sys.path.append(os.getcwd())

from core.config import setting
from services.utils.document_to_chromadb import load_or_create_chroma_vector_store
from langchain_community.callbacks import get_openai_callback

import langchain
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA, ConversationChain
from langchain.memory import ConversationBufferWindowMemory
#import logging
#logging.basicConfig()
#logging.getLogger("langchain.retrievers.multi_query").setLevel(logging.INFO)
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.storage import LocalFileStore
from core.llm import llm,embeddings
import time

# to print chain retrive context info
langchain.verbose=True



# Initialize LLM
#llm = AzureChatOpenAI(model_name='gpt-4',temperature=0)#, cache=True)
# llm=llm()

#load Chroma DB playbook data for retrival
#docsearch = load_or_create_chroma_vector_store(setting.PLAYBOOK_FILE)

############### Base vector search retriever ##################
#vecstore = Chroma(persist_directory=setting.PLAYBOOK_DB, embedding_function=embeddings,collection_name="full_documents")
vecstore = load_or_create_chroma_vector_store(setting.PLAYBOOK_FILE)
retriever=vecstore.as_retriever()

############### Multi Query Retriever ###############
from langchain.retrievers.multi_query import MultiQueryRetriever

multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=retriever, llm=llm, include_original = True
    )


def docs_qa(question:str,llm=llm):
    time_s=time.time()
    
    #initialize RetrievalQA chain
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=multi_query_retriever ,verbose=True)#, callbacks=[handler])
    #configure the system prompt for retrive context info
    qa.combine_documents_chain.llm_chain.prompt.messages[0].prompt.template="""
Use the following pieces of context to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
----------------------------------------------------------------
{context}
----------------------------------------------------------------

The user's question that you have to answer from the above pieces of context is:
"""

    with get_openai_callback() as cb:
        out=qa.invoke(question)
        
    return out['result'], cb.__dict__, time.time()-time_s

