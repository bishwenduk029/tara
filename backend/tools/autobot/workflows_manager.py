from supabase import create_client, Client
import re


class WorkflowManager:
    def __init__(self, supabase_url: str, supabase_key: str):
        self.client: Client = create_client(supabase_url, supabase_key)

    def create_workflow(self, user_id: str, status: str, comment: str, description: str):
        data = {
            'user_id': user_id.strip(),
            'status': status,
            'comment': comment,
            'description': description.strip(),
        }

        response = self.client.from_('Workflows').insert(data).execute()

        print('\nSuccessfully created new workflow')
        print("\n")
        print(response)
        return response.data[0]['id']

    def complete_workflow(self, input_string: str):
        match = re.search(r'workflow_id is (\S+)', input_string)
        if match:
            workflow_id = match.group(1)
            data, count = self.client.from_('Workflows').update({'status': 'COMPLETED'}).eq('id', workflow_id.strip()).execute()

            print('Successfully updated workflow')
            return True
        else:
            print("No workflow_id found in the input string")
            return False

supabase_url = 'https://wqttbosbkuefkspmaqfa.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndxdHRib3Nia3VlZmtzcG1hcWZhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4NzA3NTgzMCwiZXhwIjoyMDAyNjUxODMwfQ.kXfG5Y1IyJZDOFFZsG__hB87W_IHvTo8dwlZJ99woaU'
workflow_manager = WorkflowManager(supabase_url, supabase_key)