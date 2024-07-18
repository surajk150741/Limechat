import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

response_schemas = [
    ResponseSchema(name="start date", description="any start date present in the user's query. Return 'unknown' when no start date present in the query."),
    ResponseSchema(name="end date", description="any end date present in the user's query. Return 'unknown' when no end date present in the query."),
    ResponseSchema(name="end date", description="any particular date present in the user's query. Return 'unknown' when no particular date present in the query.")
]
parser = StructuredOutputParser.from_response_schemas(response_schemas)
format_instructions = parser.get_format_instructions()
prompt = PromptTemplate(
    template="You are an expert in finding out any start date, end date or any particular date present in any {input query} and convert it to defined {date format}. Take the starting of a week as start date and ending of a week as end date. If no month or year is provided, take January and 2024 respectively. If there is no date present, return 'unknown'.\n{format_instructions}",
    input_variables=["input query","date format"],
    partial_variables={"format_instructions": format_instructions}
)
chain = prompt | llm | parser
output = chain.invoke({"input query" : "How many skues are there in first week of Mach?",
                       "date format":"YYYY-MM-DD"})

print(type(output))
print(output)

