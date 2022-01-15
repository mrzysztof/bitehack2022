from flair.data import Sentence
from flair.models import TextClassifier


class InferenceModel:
    def __init__(self, path: str) -> None:
        self._model = TextClassifier.load(path)

    # returns text label
    def predict(self, text: str) -> str:
        sentence = Sentence(text, language_code='en')
        self._model.predict(sentence, mini_batch_size=1)

        label = sentence.get_label_names()[0]

        # FIXME
        mapping = {
            '0': 'not disaster',
            '1': 'disaster'
        }

        return mapping[label]