########## Required module imports #########
from langchain_openai import OpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
from langchain_core.prompts import PromptTemplate
import os
import pandas as pd
from langchain_community.agent_toolkits import create_sql_agent
from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.output_parsers import ResponseSchema, StructuredOutputParser

# ###### API key #############
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

######### Data import to be queried upon ###########
df = pd.read_excel('C:/Users/suraj/OneDrive/Desktop/Personal/bhole/gen-AI/limechat/asian_paint/Sample Data.xlsx',sheet_name='Sheet1')

######## creating sqlite db engine and saving table#########
engine = create_engine("sqlite:///asian_paints.db")
# df.to_sql("asian_paints", engine, index=False)

######### testing engine and db ##########
db = SQLDatabase(engine=engine)
print(db.dialect)
print(db.get_usable_table_names())
# print(db.run("SELECT Sales FROM asian_paints WHERE Date = '2024-06-04 00:00:00.000000' AND Region = 'Region 1';"))

# ########## defining model#############
llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

# ########## generating sql query ###########

# prompt = PromptTemplate(
#     template="""You are a SQLite expert. Given an {input} question, Create a syntactically correct SQLite query to run. You don't need to query for {top_k} results for now. Use the following format:
#     SQLQuery: SQL Query to run
# Only use the following tables:
# {table_info}
# """,
#     input_variables=["input", "table_info","top_k"]
# )
# sql_query = create_sql_query_chain(llm, db, prompt)
# response = sql_query.invoke({"question": "For Skue 10, get the difference of sales between 4th june and 13th june"})
# print(response)
# try:
#     response_split = response.split('SQLQuery:\n    ```sql\n    ')[-1]
#     try:
#         split2 = response_split.split('```')
#         final_query = split2[0]
#         print(final_query)
#         print(db.run(final_query))
#     except Exception:
#         split2 = response_split.split('\n    ```')
#         final_query = split2[0]
#         print(final_query)
#         print(db.run(final_query))
# except Exception:
#     # pass

#     try:
#         response_split = response.split('SQLQuery:\n')[-1]
#         try:
#             split2 = response_split.split('```')
#             final_query = split2[0]
#             print(final_query)
#             print(db.run(final_query))
#         except Exception:
#             split2 = response_split.split('\n    ```')
#             final_query = split2[0]
#             print(final_query)
#             print(db.run(final_query))
#     except Exception:
#         # pass

#         try:
#             response_split = response.split('SQLQuery:\n```sql\n')[-1]
#             try:
#                 split2 = response_split.split('```')
#                 final_query = split2[0]
#                 print(final_query)
#                 print(db.run(final_query))
#             except Exception:
#                 split2 = response_split.split('\n    ```')
#                 final_query = split2[0]
#                 print(final_query)
#                 print(db.run(final_query))
#         except Exception:
#             pass

# # response_split = response.split('SQLQuery:')[-1]
# # split2 = response_split.split('\n    ```')
# # final_query = split2[0]
# # print(final_query)
# # print(db.run(final_query))   ####### to check the query generated above

# ############ checking the syntax correctness of sql query########
# response_schemas = [
#     ResponseSchema(name="correct_query", description="the query after being checked. Return the update required when the query has some syntax issue.")
# ]
# parser = StructuredOutputParser.from_response_schemas(response_schemas)
# format_instructions = parser.get_format_instructions()
# prompt2 = PromptTemplate(
#     template="You are an SQLite expert. Given an {sql_query}, check if the syntax of SQL query is correct or not to run it on sqlite db for results. In case of date filters present in query, the format of dates have only date values not time e.g. 'YYYY-MM-DD'. Change the format of these date values to default python tiemstamp datetime64[ns], e.g. '2024-06-04 00:00:00.000000'. Return the sql query if it is correct and return the update required if it has some fault.\n{format_instructions}",
#     input_variables=["sql_query"],
#     partial_variables={"format_instructions": format_instructions}
# )
# chain_sql = prompt2 | llm | parser
# output = chain_sql.invoke({"sql_query" : final_query})
# print(type(output['correct_query']))
# main_query = output['correct_query']
# print('outie:',main_query)
# # # print(db.run("SELECT * FROM asian_paints LIMIT 10;"))
# # print('result:',db.run(output['correct_query']))   #### run the query on database

from langchain.memory.buffer import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain

# Initialize ConversationBufferMemory
memory = ConversationBufferMemory(
    session_id="your_session_id",  # Identifies your user or a user's session
    memory_key="history",          # Ensure this matches the key used in chain's prompt template
    return_messages=True,          # Does your prompt template expect a string or a list of Messages?
)
# # Wrap the SQL Query Chain with a ConversationChain
# # , chain=chain_sql
prompt3 = PromptTemplate(
    template="""The following is a friendly conversation between a human and an AI. The AI is smart, technical, understands and generates sql queries, talkative, provides lots of specific details from its context and replies to Human in SQL language. When human asks a question to AI or send a query to the AI, the AI refers to a table named 'asian_paints' to generate the sql query for the reply. The AI is also given 7 columns, column's datatype and example values of the columns of the table asian_paints seperated by comma as following:
    1. Region, object, 'Region 1'
    2. Pincode, int64, '123456'
    3. Date, datetime64[ns], '2024-06-04 00:00:00.000000'
    4. Skues, object, 'SKU1'
    5. Demand, int64, 250000
    6. Inventory, int64, 50000
    7. Sales, int64, 270000
    The AI should also check if the syntax of SQL query The AI generated is correct or not to run it on sqlite db for results. In case of date filters present in query, the format of dates have only date values not time e.g. 'YYYY-MM-DD'. Change the format of these date values to default python tiemstamp datetime64[ns], e.g. '2024-06-04 00:00:00.000000'.
    If the AI does not know the answer to a question, it truthfully says it does not know. Use the following format:
    response: SQL Query generated by the AI as reply to Human

Current conversation:
{history}
Human: {input}
AI Assistant:
""",
    input_variables=["input", "history"]
)
conversation_chain = ConversationChain(llm=llm,prompt=prompt3, memory=memory)
# # chain_sql2 = chain_sql | conversation_chain
# # print(chain_sql2.config)
# # chain = RunnableParallel({
# #     "sql_query": RunnablePick("sql_query"),
# #     "code": chain_sql | RunnablePick("code"),
# # }) | RunnableParallel({
# #     "language": RunnablePick("language"),
# #     "code": RunnablePick("code"),
# #     "test": test_chain | RunnablePick("test"),
# # });
output = conversation_chain.predict(input="For Skue 10, get the difference of sales between 4th june and 13th june")
o2 = output.split('```sql\n')[-1]
final_output = o2.split('\n```')[0]
final_output2 = '```'+final_output+'```'
final_output2 = final_output2.replace('\n', ' ')
final_output2 = final_output2.replace('```', '')
print("1",final_output)
print("2",final_output2)
result = db.run(final_output)
# output2 = conversation_chain.invoke({"input" : "Get it for Skue8 as well"})
print('outie2:',result)

########## execute sql query #######
# execute_query = QuerySQLDataBaseTool(db=db)
# chain = final_query | execute_query
# response = chain.invoke({"question": "How many regions are there"})
# print(response)

######### PANDAS DF##########
# date_sum = df.groupby(['Date'])['Demand','Inventory','Sales'].sum()
# pin_sum = df.groupby(['Pincode'])['Demand','Inventory','Sales'].sum()
# agent = create_pandas_dataframe_agent(
#     ChatOpenAI(temperature=0, model="gpt-4o"),
#     [df,date_sum, pin_sum],
#     verbose=True,
#     agent_type=AgentType.OPENAI_FUNCTIONS,
#     include_df_in_prompt = True,
#     number_of_head_rows = 1
# )

# agent.invoke("Give me the difference between sales of 4th june and 13th june for region 1.")
######### PANDAS DF##########