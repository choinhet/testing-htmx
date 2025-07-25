import logging

from fastapi import FastAPI, Request, Depends
from jinja2_fragments.fastapi import Jinja2Blocks
from pydantic import BaseModel

app = FastAPI()

templates = Jinja2Blocks(directory="templates")
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


class Message(BaseModel):
    count: int = 0


message = Message()


def get_message(request: Request) -> Message:
    return message


@app.get("/")
async def root(
        request: Request,
        message: Message = Depends(get_message)
):
    return templates.TemplateResponse(
        request,
        "index.html.j2",
        dict(count=message.count)
    )


@app.post("/count")
async def root(
        request: Request,
        message: Message = Depends(get_message)
):
    message.count += 1
    return templates.TemplateResponse(
        request,
        "index.html.j2",
        dict(count=message.count),
        block_name="count"
    )
