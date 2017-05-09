from normalize import Normalizer
from recognize import LetterRecognizer
from model import LetterClassifier

# creating the recognizer
# it uses `tesserocr` to provide us with very rough letter boxes
# because those boxes are pretty rough, we have to normalize them first
# by rough prediction of letter box I mean a box with 2 or more letters in it(or maybe none at all)
rec = LetterRecognizer(image_path='./res/table_real.jpg')
letters_raw = rec.find_letters()

# creating normalizer(cuts all the letters into the small images and pads them to the same size)
normalizer = Normalizer(letter_sequence=letters_raw)
letters_norm = normalizer.normalized_letters()

# creating SGD classifier model
classifier = LetterClassifier(gamma=1e-4)
classifier.load(dump_filename='model.dmp')

# resulting in labels
labels = classifier.predict(letters_norm)
