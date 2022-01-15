from pathlib import Path

from fastapi import FastAPI
from fastapi import Body
from starlette.responses import RedirectResponse
import srsly
from starlette.types import Message
import uvicorn

from models import (
    MessagesOffensivityRequest,
    MessagesOffensivityResponse
)
from model import FlairInferenceModel, TransformersInferenceModel
from config import Config


app = FastAPI(
    title='ArtificialStupidityModel',
    version='1.0',
    description='Model to detect offensive text'
)

api_directory = Path(__file__).parent
example_request = srsly.read_json(api_directory / 'data' / 'example_request.json')

config = Config()
# flair_model = FlairInferenceModel(config['flair_path'])
transformers_model = TransformersInferenceModel(config['transformers_path'])


@app.get('/', include_in_schema=False)
def docs_redirect():
    return RedirectResponse('/docs')


# TODO change name of the endpoint
@app.post('/predict', response_model=MessagesOffensivityResponse, tags=['offensivity prediction'])
async def predict(body: MessagesOffensivityRequest = Body(..., example=example_request)):
    """Detect offensive messages"""

    if hasattr(body, 'model') and body.model == 'flair':
        model = flair_model
    else:
        model = transformers_model

    results = []
    for message in body.messages:
        results.append({
            'message_id': message.message_id,
            'offensivity': model.predict(message.content)
        })

    return {
        "messages": results
    }