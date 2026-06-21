import asyncio

import numpy as np
import onnxruntime as ort

from src.config import Config


class ModelService:

    def __init__(self):
        self.model_name = Config.MODEL_NAME
        self.session = ort.InferenceSession(Config.MODEL_PATH)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    async def predict(self, input_data: np.array) -> float:
        result = await asyncio.to_thread(self.session.run, [self.output_name], {self.input_name: input_data})
        return result[0]


class ImagePreprocessedModelService(ModelService):
    MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    async def predict(self, input_data: np.array) -> float:
        input_data = (input_data - self.MEAN) / self.STD
        input_data = input_data.transpose((2, 0, 1))
        input_tensor = np.expand_dims(input_data, axis=0)
        logit = await super().predict(input_tensor)
        return self.sigmoid(logit[0][0])
