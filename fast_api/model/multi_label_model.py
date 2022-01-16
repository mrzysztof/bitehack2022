from simpletransformers.classification import MultiLabelClassificationModel
from typing import Dict


class MultiLabelModel:
    def __init__(self, path: str) -> None:
        self.model = MultiLabelClassificationModel('roberta', path, num_labels=6, use_cuda=False)

    def predict(self, text: str) -> Dict[str, bool]:
        predictions, _ = self.model.predict([text])

        return {
            name: bool(val)
            for name, val in zip(['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate'], predictions[0])
        }
