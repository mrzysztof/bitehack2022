FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Warsaw

RUN apt-get update && \
        apt-get install -y software-properties-common python3-pip git perl curl make build-essential wget gcc unzip

# COPY requirements.txt requirements.txt

# RUN pip install --no-cache-dir --upgrade -r /requirements.txt
RUN pip install --no-cache-dir --upgrade srsly fastapi==0.71.0 simpletransformers==0.63.3 uvicorn==0.17.0 gdown flair==0.10 tokenizers==0.10.1 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir --upgrade tensorflow
RUN mkdir -p code/models/ 

WORKDIR /app

COPY . .

# RUN gdown https://drive.google.com/u/1/uc?id=1epuxfPZ8gqVER1P2VQa7C9ZV753fVfDX&export=download -O /app/models/
# RUN gdown https://drive.google.com/u/1/uc?id=1gl5wmuGJlOod1uSw6w46A9PK0I3EyHKi&export=download -O /app/models/transformers-roberta-posneg.zip

# RUN unzip /app/models/transformers-roberta-posneg.zip -d roberta-text-classifier
# RUN rm /app/models/transformers-roberta-posneg.zip

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8444"]
