from io import BytesIO
from .openai_lib import *

ASSISTANT_DIAGRAM_ID        = "YOUR_ASSISTANT_ID" # Replace with your OpenAI Assistant ID
ASSISTANT_TEXT_REVIEWER_ID  = "YOUR_ASSISTANT_ID" # Replace with your OpenAI Assistant ID

if ASSISTANT_DIAGRAM_ID == "YOUR_ASSISTANT_ID" or ASSISTANT_TEXT_REVIEWER_ID == "YOUR_ASSISTANT_ID":
    raise ValueError("Please set your Assistant ID key inside the sequence.py file")

def sequence_upload_file(file_stream: BytesIO, assistant_id: str = ASSISTANT_DIAGRAM_ID):
    # 1 - Upload file to OpenAI
    file_stream.seek(0)
    uploaded_file = upload_file_in_open_ai(file_stream)
    file_id = uploaded_file.id

    # 2 - Create a new thread
    new_thread = create_thread()
    thread_id = new_thread.id
   
    # 3 - Add message with file to thread
    message = add_message_to_thread_in_opena_ai(thread_id=thread_id, 
                                                message="Generate a diagram from this code",
                                                file_id=file_id)

    # 4 - Run thread
    run_thread = run_thread_in_opena_ai(thread_id=thread_id, assistant_id=assistant_id, is_stream=True)
    
    # 5 - Retrieve thread messages
    thread_messages = list_messages_in_thread(thread_id=thread_id)
    return thread_messages

