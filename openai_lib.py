from openai import OpenAI
from io import BytesIO

OPENAI_API_KEY = "YOUR_API_KEY"  # Replace with your OpenAI API key

if OPENAI_API_KEY == "YOUR_API_KEY":
    raise ValueError("Please set your OpenAI API key inside the openai_lib.py file")

client = OpenAI(
    api_key=OPENAI_API_KEY
)
# region OWN_LOGIC 


# endregion

# region ASSISTANTS

def get_assistants():
    assistatns = client.beta.assistants.list(
        order="desc",
        limit="20")
    return assistatns

def get_assistant_by_id(id: str):
    assistant = client.beta.assistants.retrieve(id)
    return assistant

def create_assistant(name: str, model: str = "gpt-3.5-turbo", instructions: str ="", description: str = ""):
    assistant = client.beta.assistants.create(
        display_name=name,
        model=model,
        description=description,
        instructions=instructions,
    )
    return assistant

def activate_code_interpreter():
    code_interpreter = client.beta.code_interpreters.create(
        display_name="Python",
        language="python",
        supported_operations=["interpret"],
    )
    return code_interpreter

# endregion

# region THREADS

def create_thread():
    empty_thread = client.beta.threads.create()
    return empty_thread
        
def get_thread_by_id(id: str):
    thread = client.beta.threads.retrieve(id)
    return thread

def run_thread_in_opena_ai(thread_id: str, assistant_id: str):
    run_thread = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)
    return run_thread

#endregion

# region MESSAGES

def add_message_to_thread_in_opena_ai(thread_id: str, message: str, role: str = "user", file_id: str = None):
    attachments = []
    if file_id is not None:
        attachments = [{"file_id": file_id,"tools": [{"type": "code_interpreter"}]}]
    message = client.beta.threads.messages.create(  thread_id,
                                                    role=role , 
                                                    content=message,
                                                    attachments=attachments)
    return message

def retrieve_message_by_id(message_id: str, thread_id: str):
    message = client.beta.threads.messages.retrieve(
        message_id=message_id,
        thread_id=thread_id,
        )
    return message

def list_messages_in_thread(thread_id: str, run_id: str = None):
    thread_messages = client.beta.threads.messages.list(thread_id=thread_id, run_id=run_id)
    return thread_messages

# endregion

# region FILES

def upload_file_in_open_ai( file_stream: BytesIO):
    file_stream.seek(0)
    uploaded_file = client.files.create(
        file=file_stream,
        purpose="assistants"
    )
    return uploaded_file


#endregion