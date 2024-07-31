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
- For inquiries regarding the Limebot playbook, including the New Users Guide, Ambition & Approach, limebot tools, how it can be upgraded, table information etc(to be added)
"""

class playbook_query(BaseModel):
    query: str = Field(...,description="The user query related to playbook")

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
        
    def playbook_tool(self,query: str)->str:
        """
        The playbook_tool provides comprehensive guidance of a relational database having 6 tables, tables descriptions, columns and columns description, any primary or foreign key present. 
        It generates SQL queries ranging from simple to complex SQL queries using the information provided for the company database Analysis.
        """
        # self.playbook_output, self.cb_playbook, self.time_playbook= docs_qa(question=query)
        self.playbook_output, self.cb_playbook, self.time_playbook= docs_qa_sql(question=query)
        return self.playbook_output

    
 
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
                name="playbook_tool",
                args_schema=playbook_query,
                description="""
        The playbook_tool provides comprehensive guidance of a relational database having 6 tables, tables descriptions, columns and columns description, any primary or foreign key present. 
        It generates SQL queries ranging from simple to complex SQL queries using the information provided for the company database Analysis.
        """,
                func=self.playbook_tool
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
        print('playbook_test',self.playbook_output)
        if self.playbook_output != 'null':
            print('playbook_test2')
            memo_content= self.playbook_output
            memory.save_context({"input": query}, {"output": memo_content})

        final_response={'playbook_output':self.playbook_output,
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
    ans = search.playbook_tool(query)
    # ans = search.execute(query)
    return ans
    # except Exception as e:
    #     print({'function_name': 'execute', 'error_message': f"An error occurred during execute: {e}"})
    #     return {'error': str(e)}

if __name__=="__main__":
    data={
    "query": "How many tickets were in an open state in the last 2 weeks?",
    "rid": "12367",
    "email":"surajk150741@gmail.com"
}

    out=execute(**data)
    #print(json.dumps(out, indent=4))
    print('loo',out)