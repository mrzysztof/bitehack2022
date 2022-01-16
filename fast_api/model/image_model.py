import tensorflow as tf


class ImageModel:
    def __init__(self, path: str) -> None:
        self.model = tf.keras.models.load_model(path)

    def predict(self, image):
        item = self.model.predict(image)

        mapping = [
            'zero',
            'one',
            'two',
            'three',
            'four',
            'five',
            'six',
            'seven',
            'eigtht',
            'nine',
            'ten',
            'eleven',
            'twelve'
        ]

        return mapping[item]
