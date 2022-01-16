from simpletransformers.classification import ClassificationModel
import torch


class TransformersInferenceModel:
    def __init__(self, path: str):
        model_args = {"use_multiprocessing": False}
        self.model = ClassificationModel('roberta', path, num_labels=5, use_cuda=False,
                                         args=model_args)

    # returns text label
    def predict(self, text: str) -> str:
        predictions, _ = self.model.predict([text])
        
        mapping = [
            'negative',
            'fairly negative',
            'neutral',
            'fairly positive',
            'positive'
        ]

        return mapping[predictions[0]]
