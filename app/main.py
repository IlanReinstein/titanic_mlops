from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_single, predict_batch

app = FastAPI()


class SingleInput(BaseModel):
    features: list


class BatchInput(BaseModel):
    instances: list


@app.post("/predict/single")
def predict_single_item(input: SingleInput):
    return predict_single(input.features)


@app.post("/predict/batch")
def predict_batch_items(input: BatchInput):
    return predict_batch(input.instances)
