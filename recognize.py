from tesserocr import PyTessBaseAPI, RIL

from PIL import Image


class LetterRecognizer:
    def __init__(self, image_path: str, language: str = 'rus'):
        self._api = PyTessBaseAPI(lang=language)
        self._raw_image = Image.open(image_path).convert('L')
        self._api.SetImage(self._raw_image)

    def find_letters(self):
        boxes = self._api.GetComponentImages(RIL.SYMBOL, True)
        return [box[0] for box in boxes]
