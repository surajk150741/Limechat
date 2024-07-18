
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
import sys
from langchain_openai import ChatOpenAI
import openai
from langchain_openai import OpenAIEmbeddings

sys.path.append(os.getcwd())

# openai.api_key = os.environ['OPENAI_API_KEY']

# from chromadb.utils import embedding_functions
# embeddings = embedding_functions.OpenAIEmbeddingFunction(
#     model_name="text-embedding-ada-002"
# )

# llm=eval(os.getenv("LLM"))
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

embeddings=OpenAIEmbeddings
embeddings=embeddings(model="text-embedding-ada-002")


if __name__=="__main__":
    from langchain.schema import HumanMessage
    message = HumanMessage(
        content="who is building you?"
    )
    llm=llm
    print(llm.invoke([message]))
    
    embd=embeddings
    emb=embd.embed_query("what is limebote?")
    print(len(emb))
    print(emb[:5])