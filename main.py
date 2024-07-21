from typing import Union
import json, sys, os
from fastapi import FastAPI, UploadFile, Response, status
from io import BytesIO
from .docs_text import description as docs_description



app = FastAPI(
    title="OpenAI Assistant API",
    description=docs_description,
    summary="This is a simple API to interact with OpenAI Assistant")
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from openai_lib import *

@app.get("/assistants")
def get_all_assistants():
    
    assistants = get_assistants()
    print(assistants)
    return assistants

@app.get("/assistant/{id}")
def get_assistants_by_id(id: str):
    
    assistants = get_assistant_by_id(id)
    print(assistants)
    return assistants

@app.get("/thread/new-thread")
def create_new_thread():
    thread = create_thread()
    return thread

@app.post("/upload-file/{file_name}", status_code= status.HTTP_200_OK)
def upload_file(file: UploadFile, response: Response):
    if file is None or file.file is None:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {"message": "No file uploaded"}

    try:
        file_contents = file.file.read()
        file_stream = BytesIO(file_contents)
        handel_file = upload_file_in_open_ai(file_stream)
        if handel_file.status == 'processed':
            response.status_code = status.HTTP_200_OK
            return {"message": f"Successfully uploaded file to OpenAI",
                     "file_id": {handel_file.id}}
        else:
            response.status_code = status.HTTP_204_NO_CONTENT
            return {"message": f"File is not processed"}
    except Exception as ex:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
@app.post("/add-message-to-thread/{tread_id}")
def add_message_to_thread(tread_id: str, message: str, file_id: str = None):
    message = add_message_to_thread_in_opena_ai(thread_id=tread_id, message=message, file_id=file_id)
    return message

@app.post("/run-thread/{thread_id}")
def run_thread(thread_id: str, assistant_id: str):
    run_thread = run_thread_in_opena_ai(thread_id=thread_id, assistant_id=assistant_id)
    return run_thread

@app.post("/get-message/{message_id}")
def retrieve_message(message_id: str, thread_id: str):
    message = retrieve_message_by_id(message_id=message_id, thread_id=thread_id)
    return message

@app.post("/list-messages/{thread_id}")
def list_messages(thread_id: str, run_id: str = None):
    thread_messages = list_messages_in_thread(thread_id=thread_id, run_id=run_id)
    return thread_messages


@app.get("/")
def read_root():
    return {"Hello": "World"}
