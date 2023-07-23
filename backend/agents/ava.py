from langchain.agents import ConversationalAgent, Tool, AgentExecutor
from langchain import OpenAI, LLMChain
from agents.prompt import PREFIX, SUFFIX, FORMAT_INSTRUCTIONS
from agents.memory import get_ava_primary_brain
from tools.workflows import parse_execute_workflow
from tools.query import query
from tools.ingest import ingest
from tools.web_search import search_webpage
from tools.google_search import search
from tools.note_taking import parsing_record_note, parsing_search_note
from langchain.agents import load_tools
from pydantic import Field
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import SupabaseVectorStore
from langchain.tools import StructuredTool
from llama_index.langchain_helpers.memory_wrapper import GPTIndexChatMemory
from llm import llm

basic_tools = load_tools(["requests_all"])

google_search_tool = Tool(
    name="Google Search",
    description="Search Google for recent results or better understanding something.",
    func=search.run
)

tools = [search_webpage, google_search_tool,
         *basic_tools, Tool(
             name="Remember or Memorize information or content",
             func=parsing_record_note,
             description="Useful for when you need to record or memorize some information, data or note into your second brain for reference in the future. The input to this tool should be comma separated list of strings of length 2. For example `Some Note, cc9fkjdkfd`"
         ),
         Tool(
             name="Remember or Memorize content from remote location",
             func=ingest,
             description="Useful for when you need to learn or digest or ingest or memorize new information from remote locations. The input to this tool should be comma separated list of strings of length 2. For example `Some Information, cc9fkjdkfd`"
         ),
         Tool(
             name="Query or Search content from your Second Brain",
             func=query,
             description="Useful for searching through information you have already learned, memorized or ingested in your second brain. This second brain contains many documents, information or data ingested from remote location or over a course of time. The input to this tool should be comma separated list of strings of length 2. For example `Some Query, cc9fkjdkfd`"
         ), Tool(
             name="Autonomous AI agent to Execute Workflows",
             func=parse_execute_workflow,
             description="Execute the workflow autonomously for a user and for the given workflow description. The input to this tool should be comma separated list of strings of length 3. For example `Some workflow description, access token, cc9fkjdkfd`"
         )]


prompt = ConversationalAgent.create_prompt(
    tools,
    prefix=PREFIX,
    suffix=SUFFIX,
    format_instructions=FORMAT_INSTRUCTIONS,
    human_prefix="HUMAN",
    input_variables=["input", "agent_scratchpad", "chat_history"]
)

# llm_chain = LLMChain(llm=OpenAI(
#     temperature=0, model_name="gpt-4"), prompt=prompt)

llm_chain = LLMChain(llm=llm, prompt=prompt)

tool_names = [tool.name for tool in tools]
agent = ConversationalAgent(llm_chain=llm_chain, allowed_tools=tool_names)


def get_ava_for_user(user_id):
    memory = get_ava_primary_brain(user_id)
    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, tools=tools, verbose=True, memory=memory)
    return agent_executor
