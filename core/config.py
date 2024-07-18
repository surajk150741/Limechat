import os
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
LOG_PATH = os.getenv("UMM_SEARCH_LOG_PATH", "/")

class Config:
    # OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
    # LLM_CACHE_DATABASE_PATH = LOG_PATH+"LLM_cache.db"
    CHAT_MEMORY_DATABASE=os.getenv("CHAT_MEMORY_DATABASE", "")
    # CHAIN_LOG_FILE = LOG_PATH+"chain_output.log"
    # TERMINAL_LOG = LOG_PATH+"terminal.log"
    # OUTPUT_LOG = LOG_PATH+"umm_search.log"
    PLAYBOOK_FILE="documents/limebot_playbook_9th_july.txt"
    PLAYBOOK_DB="db/UMM_PLAYBOOK_10_2023_Multivector"
    SQL_CONFIG = "services/utils/config.json"
    EXAMPLES = "examples.json"
    UMM_DATABASE=os.environ.get("UMM_DATABASE", "")
    UMM_TABLE_NAME=os.environ.get("UMM_TABLE_NAME", "")
    # TOOLS_SELECTION_FILE="documents/tools_selection_queries.tsv"
    # AZURE_CLINENT= {
    #         #"api_version": os.environ.get("OPENAI_API_VERSION"),
    #         "azure_endpoint": os.environ.get("AZURE_ENDPOINT"),
    #         "azure_deployment": os.environ.get("AZURE_DEPLOYMENT"),
    #         "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
    #         "default_headers": {"OCP-Apim-Subscription-Key": os.environ.get("AZURE_OPENAI_API_KEY")},
    #     }
    # AZURE_EMBD_CLINENT= {
    #         #"api_version": os.environ.get("OPENAI_API_VERSION"),
    #         "azure_deployment": "text-embedding-3-large",
    #         "azure_endpoint": os.environ.get("AZURE_ENDPOINT"),
    #         "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
    #         "default_headers": {"OCP-Apim-Subscription-Key": os.environ.get("AZURE_OPENAI_API_KEY")},
    #     }
    # PLANNING_TOOL_MEMORY="db/planning_tool_memory.db"

setting=Config()
# print(setting.CHAT_MEMORY_DATABASE)
