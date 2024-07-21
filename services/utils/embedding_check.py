
import os
import openai
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
from chromadb.utils import embedding_functions
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    model_name="text-embedding-ada-002"
)
print('hey')
# # Define the directory for the database
# db_directory = 'path_to_your_database_directory'

# # # Initialize the Chroma search with the embedding function
# # doc_search = Chroma(persist_directory=db_directory, embedding_function=openai_ef)

# Example usage
documents = ["This is a test document.", "Another test document."]
embeddings = openai_ef(documents)
print(embeddings)