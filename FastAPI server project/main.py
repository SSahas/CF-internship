import asyncio
import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import random
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from typing import Optional
import uuid
import psutil

from query3 import user_Request
from dbms import Clients


# import time
class Input(BaseModel):
    messages: list
    stream: Optional[bool] = None
    temperature: Optional[int] = None
    context: Optional[list] = None


app = FastAPI()

BEARER_TOKEN = "Bearer asmamMSKksaksapSKmskasssmlkappie"


STREAM_DELAY = 1  # second
RETRY_TIMEOUT = 15000  # milliseconds


# List of random words for demonstration purposes
random_words = ["apple", "banana", "cherry", "date",
                "elderberry", "fig", "grape", "honeydew", "kiwi", "lemon"]


async def get_random_word():
    return random.choice(random_words)


async def word_generator():

    word = await get_random_word()
    print(word)
    time_gap = random.uniform(0, 1)
    await asyncio.sleep(time_gap)
    return word




# input_queue = asyncio.Queue()  # Queue to hold incoming messages


async def verify_headers(request):
    request_token = request.headers['authorization']

    if request_token == BEARER_TOKEN:
        return JSONResponse(status_code=200, content="authorization successful")

    elif request_token[0:7] != "Bearer":
        raise HTTPException(
            status_code=400, detail="Bad Request,incorrect token format, format required Bearer <API KEY>")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized Request")

connected_clients = {}


async def users(client_id, question):
    if client_id not in connected_clients:
        connected_clients[client_id] = {
            "Questions": asyncio.Queue(), "Answers": asyncio.Queue()}

    await connected_clients[client_id]["Questions"].put(question)


@app.get("/")
async def root(request: Request):
    return await verify_headers(request)


async def event_generator(input_queue):
    while True:
        # Check if there are new messages from input
        new_message = await input_queue.get()
        if new_message[0] is True:
            yield {
                "event": "new_messages",
                "id": "message_id",
                "retry": RETRY_TIMEOUT,
                "data": new_message[1]
            }
            break
        else:
            yield {
                "event": "new_messages",
                "id": "message_id",
                "retry": RETRY_TIMEOUT,
                "data": new_message[1]
            }


async def get_answers(input_queue=None):
    count = 0
    final_value = ""

    while count < 5:
        message_word = await word_generator()
        if input_queue:
            await input_queue.put((False, message_word))
        final_value += message_word + ", "
        count += 1

    message_word = await word_generator()
    if input_queue:
        await input_queue.put((True, message_word))
    final_value += message_word + ", "

    return final_value


async def stream_response():
    input_queue = asyncio.Queue()
    asyncio.create_task(get_answers(input_queue))
    return EventSourceResponse(event_generator(input_queue))


async def get_response(stream):
    if stream == True:
        return await stream_response()
    else:
        return await get_answers()


@app.get('/question')
async def message_stream(request: Request, data: Input):
    

    response = await get_response(stream=bool(data.stream))

    return response


async def check_resources(cpu_before, cpu_after, ram_before, ram_after):

    cpu_used = cpu_after - cpu_before
    ram_used = ram_after - ram_before

    return cpu_used, ram_used


@app.get("/heart")
async def usage(request: Request):

    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        
    }


if __name__ == "__main__":
    
    uvicorn.run(app, host="localhost", port=8000)



