import numpy as np

from tesserocr import PyTessBaseAPI, RIL

from PIL import Image

image = Image.open('./res/table_real.jpg').convert('L')

api = PyTessBaseAPI(lang='rus')
api.SetImage(image)

boxes = api.GetComponentImages(RIL.SYMBOL, True)

print('Found {} textline image components.'.format(len(boxes)))

for i, (im, box) in enumerate(boxes):
    api.SetRectangle(box['x'], box['y'], box['w'], box['h'])
    ocrResult = api.GetUTF8Text()
    conf = api.MeanTextConf()

    res_arr = np.zeros((1028, 30))
    res_img = Image.fromarray(res_arr)
