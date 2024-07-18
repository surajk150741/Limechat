import pandas as pd
import openai

import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")

# Define the NLQ (Natural Language Query)
nlq = "How many rows are there in accounts table?"

# Define schema_context
path = ['accounts','contacts','conversations','inboxes','messages']
schemas = {}
for p in path:
    d2 = {}
    df = pd.read_csv(f"{p}.csv")
    c = list(df.columns.values)
    d2['columns']=c
    schemas[p]=d2
schema_context = "\n".join([
    f"- Table: {table}\n  - Columns: {', '.join(schema['columns'])}"
    for table, schema in schemas.items()
])
# print(schemas)
# print(schema_context)
prompt=f"Convert the following NLQ into a SQL query:\n\"{nlq}\"\n\nDatabase Schema:\n{schema_context}\n\nSQL Query:"
    
# Generate SQL query using GPT-3
response = openai.Completion.create(
    engine="davinci",  # or use another appropriate engine
    prompt=prompt,
    max_tokens=50  # You can adjust this based on your needs
)

sql_query = response.choices[0].text.strip()
print("Generated SQL Query:", sql_query)