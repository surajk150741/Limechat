import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain.chains import SimpleChain
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# TEMPLATE = """You are an expert in finding out the date terms present in any string or sentence. Given an {input query}, extract any phrase or word from the query that means following terms:
# 1. Start Date
# 2. End Date
# 3. Any particular date(including today, tomorrow etc)
# After getting the phrase, convert it into the format YYYY-MM-DD.
# """

# PROMPT = PromptTemplate(
#     input_variables=["input query"], template=TEMPLATE
# )
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "You are an expert in finding out any start date, end date or any particular date present in any sentence, convert it to defined {date format} and providing the result as a dictionary with 'start date','end date', 'particular date' as keys.",
#         ),
#         ("human", "{input query}"),
#     ]
# )
# chain = prompt | llm
# response = chain.invoke(
#     {
#         "input query": "How many ice cream were sold on 15th feb",
#         "date format": "YYYY-MM-DD"
#     }
# )
# print(response)

#### JSON PARSER####
# Define your desired data structure.

# class dates(BaseModel):
#     start_date: str = Field(description="if any start date present")
#     end_date: str = Field(description="if any end date is present")
#     particular_date: str = Field(description="if any particular date is present")

# # And a query intented to prompt a language model to populate the data structure.
# input_query = "How many ice cream were sold on 15th Jan?"
# date_format = "YYYY-MM-DD"

# # Set up a parser + inject instructions into the prompt template.
# parser = JsonOutputParser(pydantic_object=dates)

# prompt = PromptTemplate(
#     template="You are an expert in finding out any start date, end date or any particular date present in any {input_query} and convert it to defined {date_format}.If there is no date present, return 'unknown'.\n{format_instructions}",
#     input_variables=["input_query","date_format"],
#     partial_variables={"format_instructions": parser.get_format_instructions()},
# )

# chain = prompt | llm | parser

# output = chain.invoke({"input_query" : input_query,
#                        "date_format":date_format})
# print(output)
#### JSON PARSER####

# parser = PydanticOutputParser(pydantic_object=dates)
# format_instructions = parser.get_format_instructions()

# prompt = PromptTemplate(
#     template="You are an expert in finding out any start date, end date or any particular date present in any {input query} and convert it to defined {date format}.If there is no date present, return 'unknown'.\n{format_instructions}",
#     input_variables=["input query","date format"],
#     partial_variables={"format_instructions": format_instructions}
# )
# chain = prompt | llm | parser

# output = chain.invoke({"input query" : "ice cream flavors",
#                        "date format":"YYYY-MM-DD"})
# print(type(output))
# print(output)
