from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
from tools.autobot.agent import AutoGPT
from langchain.chat_models import ChatOpenAI
from langchain.tools.file_management.write import WriteFileTool
from langchain.tools.file_management.read import ReadFileTool
from tools.notion_client import update_or_create_page
from tools.web_search import search_webpage
from tools.google_search import search
import faiss
from langchain.tools import Tool
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import load_tools
import asyncio
from langchain.requests import TextRequestsWrapper
from tools.requests_get import RequestsGetTool
from langchain.tools.base import BaseTool
from tools.get_google_access_token import get_access_token
from llm import llm

def _get_tools_requests_get() -> BaseTool:
    return RequestsGetTool()

requests_tools = load_tools(["requests_post", "requests_patch", "requests_put", "requests_delete"])

google_search_tool = Tool(
    name = "Google Search",
    description="Search Google for recent results or better understanding something.",
    func=search.run
)

def initialize_agent():
    embeddings_model = OpenAIEmbeddings()
    embedding_size = 1536
    index = faiss.IndexFlatL2(embedding_size)
    vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})
    
    tools = [
        WriteFileTool(),
        ReadFileTool(),
        update_or_create_page,
        google_search_tool,
        search_webpage,
        *requests_tools,
        _get_tools_requests_get()
    ]
    
    agent = AutoGPT.from_llm_and_tools(
        ai_name="Ava",
        ai_role="Virtual Assistant",
        tools=tools,
        # llm=ChatOpenAI(model_name="gpt-4", temperature=0),
        llm=llm,
        memory=vectorstore.as_retriever()
    )
    agent.chain.verbose = True
    
    return agent

agent = initialize_agent()

async def process_objective(objective: str, access_token: str, user_id: str, workflow_id: str):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, agent.run, [objective + "\nuserID is " + user_id + "\nWhen needed google access token is " + access_token + "\nworkflow_id is " + workflow_id])
