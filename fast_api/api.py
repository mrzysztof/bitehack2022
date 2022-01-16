from audioop import mul
from pathlib import Path
from urllib import response
import base64
import io

from fastapi import FastAPI
from fastapi import Body
from starlette.responses import RedirectResponse
import srsly
from starlette.types import Message
import uvicorn

from PIL import Image
import numpy as np

from models import (
    MessagesOffensivityRequest,
    MessagesOffensivityResponse,
    MessagesFilledRequest,
    MessagesFilledResponse,
    ImagesEmotionsRequest,
    ImagesEmotionsResponse,
    MessagesOffensiveResponse
)
from model import (
    FlairInferenceModel, 
    TransformersInferenceModel, 
    LanguageModel, 
    ImageModel,
    MultiLabelModel
)
from config import Config


app = FastAPI(
    title='ArtificialStupidityModel',
    version='1.2',
    description='Model to detect offensive text'
)

api_directory = Path(__file__).parent
example_request = srsly.read_json(api_directory / 'data' / 'example_request.json')

config = Config()
flair_model = FlairInferenceModel(config['flair_path'])
transformers_model = TransformersInferenceModel(config['transformers_path'])
language_model = LanguageModel(config['language_model_path'])
# image_model = ImageModel(config['image_model_path'])
multi_label_model = MultiLabelModel(config['multi_label_path'])


@app.get('/', include_in_schema=False)
def docs_redirect():
    return RedirectResponse('/docs')


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

@app.post('/lm', response_model=MessagesFilledResponse, tags=['language model'])
async def lm(body: MessagesFilledRequest = Body(...)):
    """Insert words in the place of offensive ones"""

    results = []
    for message in body.messages:
        results.append({
            'message_id': message.message_id,
            'content': language_model.predict(message.content, message.spans)
        })

    return {
        "messages": results
    }

@app.post('/image', response_model=ImagesEmotionsResponse, tags=['emotions prediction'])
async def image(body: ImagesEmotionsRequest = Body(...)):
    """Detects emotions based on the people's faces"""

    results = []
    for image in body.images:
        decoded = base64.decodebytes(image.image)
        image = Image.open(io.BytesIO(decoded))

        im = np.array(image, dtype=np.uint8)

        results.append({
            'image_id': image.image_id,
            'emotion': image_model.predict(im)
        })

    return {
        "images": results
    }

@app.post('/offensive', response_model=MessagesOffensiveResponse, tags=['offensive language detection'])
async def offensive(body: MessagesOffensivityRequest = Body(..., example=example_request)):
    """Detects offensive language"""

    results = []
    for message in body.messages:
        print(multi_label_model.predict(message.content))
        results.append({
            'message_id': message.message_id,
            'labels': multi_label_model.predict(message.content)
        })

    return {
        "messages": results
    }
