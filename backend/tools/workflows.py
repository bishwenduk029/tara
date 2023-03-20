from pydantic import BaseModel, Field
from tasks import process_objective
import asyncio
from langchain.tools import tool
from tools.autobot.workflows_manager import workflow_manager

class WorkflowDescription(BaseModel):
    content: str
    access_token: str
    user_id: str

def execute_workflow(workflow_description: str, access_token: str, user_id: str) -> dict:
    """Execute the workflow autonomously for a user and for the given workflow description"""

    new_workflow_id = workflow_manager.create_workflow(user_id, "PROCESSING", "", workflow_description)
    
    # Step 1: Search for an existing page with the given title
    asyncio.create_task(process_objective(workflow_description, access_token, user_id, new_workflow_id))
    return "Workflow processing initialized for workflow-id " + new_workflow_id + " . Politely ask the user to wait as the workflow is being executed and share the workflow-id with them"


def parse_execute_workflow(input: str):
    workflow_description, access_token, user_id = input.rsplit(",", 2)
    return execute_workflow(workflow_description.strip(), access_token.strip(), user_id.strip())