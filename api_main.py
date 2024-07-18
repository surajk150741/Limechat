from fastapi import FastAPI, Request, Path, HTTPException
import uvicorn
import os
import time
app=FastAPI()
from langchain_openai import ChatOpenAI
from langchain.memory.buffer import ConversationBufferMemory
from langchain.chains.conversation.base import ConversationChain
from langchain_core.prompts import PromptTemplate
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd

import http.server
import socketserver
from limebot import search_core
query='How many tickets were in an open state in the last 2 week?'
rid = '1223456'
email = 'surajk150741@gmail.com'
search_core = search_core(query=query,rid=rid,email=email)

out = search_core.playbook_tool(query=query)
print('SQLQuery:',out)

# out = search_core.database_tool(query=query)
# print('Result:',out)

# PORT = 8000
# Handler = http.server.SimpleHTTPRequestHandler

# with socketserver.TCPServer(("", PORT), Handler) as httpd:
#     print("serving at port", PORT)
#     httpd.serve_forever()

# llm = ChatOpenAI(
#     model="gpt-4o",
#     temperature=0
# )

# @app.get('/search_report_generation')
# def report_generation(nlq: str):
#     time_s=time.time()
#     final_output = "it's working"
#     return final_output
# templates = Jinja2Templates(directory="C:/Users/suraj/OneDrive/Desktop/Personal/bhole/gen-AI/limechat")
# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     # Render the HTML template
#     return templates.TemplateResponse("index.html", {"request": request})
# if __name__=='__main__':
#     uvicorn.run("api_main:app", host='localhost', port=7000, reload=False, workers=1)