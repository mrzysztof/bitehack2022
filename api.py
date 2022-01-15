from pathlib import Path

from fastapi import FastAPI
from fastapi import Body
from starlette.responses import RedirectResponse
import srsly
from starlette.types import Message
import uvicorn

from models import (
    MessagesOffensivityRequest,
    MessagesOffensivityResponse,
    TableRecognitionRequest,
    TablesContentAndPositionResponse
)
from model import FlairInferenceModel, TransformersInferenceModel


app = FastAPI(
    title='ArtificialStupidityModel',
    version='1.0',
    description='Model to detect offensive text'
)

api_directory = Path(__file__).parent
example_request = srsly.read_json(api_directory / 'data' / 'example_request.json')

flair_model = FlairInferenceModel()
transformers_model = TransformersInferenceModel()


@app.get('/', include_in_schema=False)
def docs_redirect():
    return RedirectResponse('/docs')


# TODO change name of the endpoint
@app.post('/predict', response_model=MessagesOffensivityResponse, tags=['offensivity prediction'])
async def offensive_predict(body: MessagesOffensivityRequest = Body(..., example=example_request)):
    """Detect offensive messages"""

    

    return {"tables": tables}