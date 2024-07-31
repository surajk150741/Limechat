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
data={
"query": "How many tickets were handed off to agents on 10th October?",
"rid": "12353",
"email":"surajk150741@gmail.com"
}
search_core = search_core(query=data["query"],rid=data["rid"],email=data["email"])
# out=search_core.execute(data["query"])
# print('uio',out)
output = search_core.execute(data["query"])
final_sql = output['SQL']
answer = output['llm_generate_output']
print('f1',final_sql)
print('f2',answer)

# @app.get('/search_report_generation')
# def report_generation(nlq: str):
#     time_s=time.time()
#     output = search_core.execute(nlq)
#     final_sql = output['SQL']
#     answer = output['llm_generate_output']
#     elapsed_time = time.time() - time_s
#     print(f"Execution time: {elapsed_time} seconds")
#     return final_sql, answer
# templates = Jinja2Templates(directory="C:/Users/suraj/OneDrive/Desktop/Personal/bhole/gen-AI/limechat")
# @app.get("/", response_class=HTMLResponse)
# async def read_root(request: Request):
#     # Render the HTML template
#     return templates.TemplateResponse("index.html", {"request": request})
# if __name__=='__main__':
#     uvicorn.run("api_main:app", host='localhost', port=7000, reload=False, workers=1)

