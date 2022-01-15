from typing import List, Optional, Union
from pydantic import BaseModel, Field


class MessageOffensivityRequest(BaseModel):
    message_id: int
    content: str


class MessagesOffensivityRequest(BaseModel):
    messages: List[MessageOffensivityRequest]
    

class APIMessage(BaseModel):
    message: str


class SpanResponse(BaseModel):
    start: int
    end: int


class MessageOffensivityResponse(BaseModel):
    message_id: int
    offensivity: str
    peaks: Optional[List[SpanResponse]]


class MessagesOffensivityResponse(BaseModel):
    messages: List[MessageOffensivityResponse]
    model: Optional[str]
    errors: Optional[List[APIMessage]]
    warnings: Optional[List[APIMessage]]
