from typing import List, Optional, Union
from pydantic import BaseModel, Field


class MessageOffensivityRequest(BaseModel):
    message_id: int
    content: str


class MessagesOffensivityRequest(BaseModel):
    messages: List[MessageOffensivityRequest]
    model: Optional[str]
    

class APIMessage(BaseModel):
    message: str


class Span(BaseModel):
    start: int
    end: int


class MessageOffensivityResponse(BaseModel):
    message_id: int
    offensivity: str
    peaks: Optional[List[Span]]


class MessagesOffensivityResponse(BaseModel):
    messages: List[MessageOffensivityResponse]
    errors: Optional[List[APIMessage]]
    warnings: Optional[List[APIMessage]]


# /lm communication

class MessageFilledRequest(BaseModel):
    message_id: int
    content: str
    spans: List[Span]


class MessagesFilledRequest(BaseModel):
    messages: List[MessageFilledRequest]


class MessageFilledResponse(BaseModel):
    message_id: int
    content: str


class MessagesFilledResponse(BaseModel):
    messages: List[MessageFilledResponse]
    errors: Optional[List[APIMessage]]
    warnings: Optional[List[APIMessage]]

# /image communication

class ImageEmotionsRequest(BaseModel):
    image_id: int
    image: str


class ImagesEmotionsRequest(BaseModel):
    images: List[ImageEmotionsRequest]


class ImageEmotionsResponse(BaseModel):
    image_id: int
    emotion: str


class ImagesEmotionsResponse(BaseModel):
    images: List[ImageEmotionsResponse]
    errors: Optional[List[APIMessage]]
    warnings: Optional[List[APIMessage]]


# /offensive communication

class OffensivityLabels(BaseModel):
    toxic: bool
    severe_toxic: bool
    obscene: bool
    threat: bool
    insult: bool
    identity_hate: bool


class MessageOffensiveResponse(BaseModel):
    message_id: int
    labels: OffensivityLabels


class MessagesOffensiveResponse(BaseModel):
    messages: List[MessageOffensiveResponse]
    errors: Optional[List[APIMessage]]
    warnings: Optional[List[APIMessage]]
