import json
import time
import os
import sys
sys.path.append(os.getcwd())


# from services.utils.add_group_type import AddGroupType
# from services.utils.SQL_helper import extract_sql_query, add_country_brand_name
from langchain_community.callbacks import get_openai_callback
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from few_shot_sql_examples import examples_selector
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain.chains import LLMChain
from typing import Optional
from core.config import setting
from core.llm import llm, embeddings

mysql_str="mysql://root:Qwert1234%@localhost:3306/limechat2"
# tables="accounts"

db_data = SQLDatabase.from_uri("mysql://root:Qwert1234%@localhost:3306/limechat2")

with open(setting.SQL_CONFIG, 'r') as json_file:
    config = json.load(json_file)
    

def generate_sql_from_db(query:str, llm=llm, handler=None, config=config["using_DB"]):
    """
    Generate SQL from the database based on the provided query.

    Args:
        query (str): The user query.
        llm (ChatOpenAI): Language model instance.
        handler: Callback handler (if any).
        config (dict): Configuration settings.

    Returns:
        tuple: Tuple containing final SQL and extracted SQL.
    """

    db = SQLDatabase.from_uri(
        mysql_str,
        sample_rows_in_table_info=1
        )
    
    example_prompt = PromptTemplate.from_template("User input: {input}\nSQL query: {query}")

    with open(setting.EXAMPLES, 'r') as json_file:
        examples = json.load(json_file)
    examples=examples["examples"]

    prefix = r"""
You are a mysql expert. You are also trained for reading the schema of a mysql relational database of 6 tables. Given an input question, first create a syntactically correct mysql query to run, then look at the results of the query and return the answer. Unless otherwise specificed, do not return more than {top_k} rows.
Use the following format:

Question: "Question here"
SQLQuery: "SQL Query to run"

Also, the tables, the table's description, their columns and their primary & foreign keys are provided as well. Each table is seperated by it's next table features by a new line character in order as follows:
-------------------------------------------------
"""+ str(config["schema_describtion"])+ r"""
-------------------------------------------------

Here is the relevant table info: {table_info}

Below are a number of examples of questions and their corresponding SQL queries.
    """

    suffix = """
NOTE: In case of date filters present in query, use the default python timestamp datetime64[ns] format for these date values to , e.g. '2024-06-04 00:00:00.000000'.
Return only SQL query, nothing else.

Question: ```{input}```,
SQL Query: 
    """
    prompt = FewShotPromptTemplate(
        examples=examples[:10],
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=["input", "top_k", "table_info"],
    )

    db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db,prompt=prompt, verbose=True ,return_sql=True, return_direct=True, return_intermediate_steps=False, use_query_checker=True)#,callbacks=[handler])
    
    result=db_chain.invoke(query)
    
    sql=result['result'] #.replace('\n',' ')
    sql = sql.replace("```sql\n",'')
    sql = sql.replace("```SQL",'')
    sql = sql.replace("\n```",'')
    sql = sql.replace("\n","")
    # print('yeeiis',sql)
    out=f"""
    SQLQuery: {sql},

    SQLResult:  {db_data.run(sql)}
    """
    return out, sql

if __name__=='__main__':
    
    query = "How many tickets were in an open state in the last 2 week?"
    out=generate_sql_from_db(query)
    print('out',out[0])