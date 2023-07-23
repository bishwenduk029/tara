import base64
import json
import time
import logging

from fastapi import FastAPI, UploadFile, BackgroundTasks, Header, Depends, HTTPException, Header
from jose import JWTError, jwt
from typing import Optional
from supabase_client import supabase
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from ai import get_completion
from stt import transcribe
from tts import to_speech

app = FastAPI()
origins = [
    "http://localhost:3000",  # React app address
    # any other origins that need access to the API
]

SECRET_KEY = "xoiq9aYf82Zfz0oTQ8fCCe4Q0/CKfnATSwEQjqGHIhaC9BDXSMLNK1mqtuDIIhq5bXKItSpFUPq88nJCBc6WRA=="
ALGORITHM = "HS256"


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logging.basicConfig(level=logging.INFO)


def get_current_user(authorization: Optional[str] = Header(None)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # if not authorization:
    #     raise credentials_exception
    print(authorization)
    scheme, token = authorization.split()
    print(scheme.lower() != 'bearer')
    if scheme.lower() != 'bearer':
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[
                             ALGORITHM], options={"verify_aud": False})
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError as e:
        print(e)
        raise credentials_exception


@app.post("/inference")
async def infer(audio: UploadFile, background_tasks: BackgroundTasks,
                user_id: str = Depends(get_current_user)) -> FileResponse:
    logging.debug("received request")
    start_time = time.time()

    user_prompt_text = await transcribe(audio)
    ai_response_text = await get_completion(user_prompt_text, user_id)
    ai_response_audio_filepath = await to_speech(ai_response_text, background_tasks)

    logging.info('total processing time: %s %s',
                 time.time() - start_time, 'seconds')
    return FileResponse(path=ai_response_audio_filepath, media_type="audio/mpeg",
                        headers={"text": _construct_response_header(user_prompt_text, ai_response_text)})


@app.get("/")
async def root():
    return RedirectResponse(url="/index.html")


class ChatInput(BaseModel):
    user_message: str


@app.post("/chats")
async def api_process_objective(chat_input: ChatInput, user_id: str = Depends(get_current_user)):
    """
    Process objective and provide guidance
    """
    ai_response_text = await get_completion(chat_input.user_message, user_id)
    return ai_response_text


app.mount("/", StaticFiles(directory="/Users/kundb/projects/tara/frontend/dist"), name="static")


def _construct_response_header(user_prompt, ai_response):
    return base64.b64encode(
        json.dumps(
            [{"role": "user", "content": user_prompt}, {"role": "assistant", "content": ai_response}]).encode(
            'utf-8')).decode("utf-8")
