
import json
from core.config import setting
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings

# with open(setting.EXAMPLES, 'r') as json_file:
#     examples = json.load(json_file)
# print(examples["examples"])

vector_store = FAISS
def examples_selector():

    # example_selector = SemanticSimilarityExampleSelector.from_examples(
    #     examples,
    #     OpenAIEmbeddings(),
    #     vector_store,
    #     k=k,
    #     input_keys=["input"],
    # )
    with open(setting.EXAMPLES, 'r') as json_file:
        examples = json.load(json_file)
    examples=examples["examples"]
    return SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        vector_store,
        k=4,
        input_keys=["input"]
    )

# example_selector.select_examples({"input": "how many artists are there?"})


############################ BELOW IS FOR UPDATING THE examples.json FILE USING PYTHON ################################
# examples = [
#     {"input": "List all artists.", "query": "SELECT * FROM Artist;"},
#     {
#         "input": "Find all albums for the artist 'AC/DC'.",
#         "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",
#     },
#     {
#         "input": "List all tracks in the 'Rock' genre.",
#         "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",
#     },
#     {
#         "input": "Find the total duration of all tracks.",
#         "query": "SELECT SUM(Milliseconds) FROM Track;",
#     },
#     {
#         "input": "List all customers from Canada.",
#         "query": "SELECT * FROM Customer WHERE Country = 'Canada';",
#     },
#     {
#         "input": "How many tracks are there in the album with ID 5?",
#         "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",
#     },
#     {
#         "input": "Find the total number of invoices.",
#         "query": "SELECT COUNT(*) FROM Invoice;",
#     },
#     {
#         "input": "List all tracks that are longer than 5 minutes.",
#         "query": "SELECT * FROM Track WHERE Milliseconds > 300000;",
#     },
#     {
#         "input": "Who are the top 5 customers by total purchase?",
#         "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",
#     },
#     {
#         "input": "Which albums are from the year 2000?",
#         "query": "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",
#     },
#     {
#         "input": "How many employees are there",
#         "query": 'SELECT COUNT(*) FROM "Employee"',
#     },
# ]
# data = {"examples": examples}

# # Open a file in write mode
# with open('examples.json', 'w') as json_file:
#     # Write the dictionary to the file
#     json.dump(data, json_file, indent=4)
############################ ABOVE IS FOR UPDATING THE examples.json FILE USING PYTHON ################################