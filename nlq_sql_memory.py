import os
import sys
sys.path.append(os.getcwd())

import json
import time
from core.llm import llm
from memory import CustomMessageConverter
from core.config import setting
from nlq_to_sql import generate_sql_from_db
# from doc_QA import docs_qa
from doc_QA_sql import docs_qa_sql
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import tool, Tool, BaseTool, StructuredTool
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory, ConversationBufferWindowMemory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.callbacks import FileCallbackHandler, get_openai_callback
import os
# from langchain.utilities import SQLDatabase
# from langchain.llms import OpenAI
# from langchain_experimental.sql import SQLDatabaseChain

# db = SQLDatabase.from_uri("sqlite:///output.db")
# llm = OpenAI(temperature=0, verbose=True)
# db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)
# print(db_chain)
# db_chain.run("Describe the conversation table")

system_prompt="""
You are helpful conversational assistant for helping Limebot platform regarding following tasks:
- To explore data related to all the conversations of customers with clients, inbox information about each accounts/clients, the database_tool is to be used.
"""

class database_query(BaseModel):
    query: str = Field(...,description="The user query regarding database related information")

# llm=llm(model="gpt-4",temperature=0,cache=True,verbose=True)
prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")])


class search_core:
    def __init__(self,query:str,rid:str,email:str):
        self.query=query
        self.rid = rid
        self.email = email
        # self.countries=countries
        # self.brands=brands
        # self.planning_tool_profile_info={'profile_id':profile_id,
        #                     'age':age,
        #                     'audience':audience,
        #                     'name':name,
        #                     'mode_type':mode_type}
        
        self.playbook_output, self.cb_playbook, self.time_playbook='null',{},0
        self.sql, self.cb_db, self.time_db= 'null',{},0
        
    def database_tool(self, query: str)->str:
        """
        To explore data related to all the conversations of customers with clients, inbox information about each accounts/clients, the database_tool is to be used.
        It provides insights and analysis to optimize marketing strategies and enhance decision-making processes. It also generates SQL query to be run on db for getting the final output.
        """
        # self.generate_sql, self.cb_db, self.time_db=generate_sql_from_db(query)
        self.generate_sql=generate_sql_from_db(query)
        self.sql=self.generate_sql[0]
        
        return self.generate_sql[0]
    
 
    def execute(self,query:str):
        
        time_s=time.time()
        
        chat_message_history = SQLChatMessageHistory(
            session_id=self.rid,
            connection_string=setting.CHAT_MEMORY_DATABASE,
            custom_message_converter=CustomMessageConverter(author_email=self.email),
        )
        
        memory = ConversationBufferWindowMemory(
            k=6,
            memory_key="chat_history",
            chat_memory=chat_message_history,
            return_messages=True
        )
        
        tools = [
            Tool(
                name="database_tool",
                args_schema=database_query,
                description="""
        To explore data related to all the conversations of customers with clients, inbox information about each accounts/clients, the database_tool is to be used. (by using database_tool) etc(to be added) 
        It provides insights and analysis to optimize marketing strategies and enhance decision-making processes. It also generates SQL query to be run on db for getting the final output.
        """,
                func=self.database_tool
            )
        ]
        
        agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True, return_intermediate_steps=True)

        with get_openai_callback() as cb:
            output=agent_executor.invoke({'input':query,'chat_history':memory.load_memory_variables({})['chat_history']})
        
        print(output['chat_history'],'\n\n')
        
        time_taken = {
            'playbook_QA': self.time_playbook,
            'query_to_sql': self.time_db
        }
        
        LLM_uses={
            'Agent_Executor': cb.__dict__,
            'Platbook_Tool': self.cb_playbook,
            'database_tool': self.cb_db
        }
        if self.sql != 'null':
            print('jadoo')
            memo_content= json.dumps(self.generate_sql[0])
            memory.save_context({"input": query}, {"output": memo_content})

        final_response={'SQL': self.sql,
                        'llm_generate_output': output['output']}
        

        return final_response

def execute(query: str,rid:str,email:str):
    """
    Execute the search operation with error handling.

    Args:
        query (str): The user query.

    Returns:
        dict: The search output.
    """
    search=search_core(query,rid,email)
    # ans = search.database_tool(query)
    ans = search.execute(query)
    return ans
    # except Exception as e:
    #     print({'function_name': 'execute', 'error_message': f"An error occurred during execute: {e}"})
    #     return {'error': str(e)}

if __name__=="__main__":
    data={
    "query": "And what about 12th October?",
    "rid": "12374",
    "email":"surajk150741@gmail.com"
}

    out=execute(**data)
    #print(json.dumps(out, indent=4))
    print(out)