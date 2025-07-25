import logging
from typing import List, Annotated

from fastapi import FastAPI, Request, Depends, Form
from jinja2_fragments.fastapi import Jinja2Blocks
from pydantic import BaseModel, Field

app = FastAPI()

templates = Jinja2Blocks(directory="templates")
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)


class Contact(BaseModel):
    name: str
    email: str


def get_some_contacts() -> List[Contact]:
    return [
        Contact(name="John", email="jd@gmail.com"),
        Contact(name="Clara", email="cd@gmail.com"),
    ]


def has_email(contacts: List[Contact], email: str) -> bool:
    for contact in contacts:
        if email == contact.email:
            return True
    return False


class Message(BaseModel):
    contacts: List[Contact] = Field(default_factory=get_some_contacts)


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
        message.model_dump()
    )


@app.post("/contacts")
async def contacts(
        request: Request,
        name: Annotated[str, Form()],
        email: Annotated[str, Form()],
        message: Message = Depends(get_message)
):
    if has_email(message.contacts, email):
        return templates.TemplateResponse(
            request,
            "index.html.j2",
            message.model_dump(),
            block_name="display",
            status_code=422,
        )

    message.contacts.append(Contact(name=name, email=email))
    return templates.TemplateResponse(
        request,
        "index.html.j2",
        message.model_dump(),
        block_name="display",
    )
