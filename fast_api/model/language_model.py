from typing import Dict
from transformers import pipeline


class LanguageModel:
    def __init__(self, path: str):
        self.fill_mask = pipeline(
            "fill-mask",
            model="roberta-base",
            tokenizer="roberta-base"
        )

    def _replace(self, text, start, end, subst):
        return f'{text[:start]}{subst}{text[end:]}'

    # returns filled text
    def predict(self, text: str, spans: Dict[str, int]) -> str:
        off = 0
        for span in spans:
            start, end = span.start + off, span.end + off
            old_length = end - start

            replaced = self._replace(text, start, end, '<mask>')

            predictions = self.fill_mask(replaced)

            replacement = predictions[0]["token_str"]
            for i in range(len(predictions)):
                word = predictions[i]["token_str"]
                if all(not swear in word for swear in ['fuck', 'bitch', 'ass']):
                    replacement = word
                    break

            text = self._replace(text, start, end, replacement)
            off = len(replacement) - old_length

        return text
