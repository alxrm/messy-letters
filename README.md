# russian-letters-classifier
[![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)]()

### Story

— so the task is __to count all underlined and strikethrough letters from the image__        
— okay, sounds cool, but what is the image?        
— well, it's gonna be something like [this](https://github.com/alxrm/messy-letters-classifier/blob/master/res/table.jpg)        
— so I have to cut all the letters out, know their positions, normalize the pictures of letters and then just feed them to the trained classifier, gonna be easy        

## Project

_That's right, the repository is mostly about the last part of this "conversation", except it doesn't contain datasets and trained model._

### Letter recognition

So to do _something_, I had to recognize letters and get their positions. Before I knew what real table would be, I've tried to do it manually.        


It was thrown away as a really bad idea as soon, as I've seen [this](https://github.com/alxrm/messy-letters-classifier/blob/master/res/table_real.jpg), so I decided to use [tesseract](https://github.com/tesseract-ocr/tesseract), because it has the ability to recognize russian letters. There's small [wrapper](https://github.com/alxrm/messy-letters-classifier/blob/master/recognize.py) above the `tesseract` python API.


It worked pretty well, but some of the recognized boxes were unable to use, they had more than one letter or sometimes there were no letters at all. So it should be filtered somehow.

### Normalizer

Next step is to create something, that returns the same letter sequence(preserving order), but contains only normalized letters, without any junk. So here comes the [normalizer](https://github.com/alxrm/messy-letters-classifier/blob/master/normalize.py).


It receives `letter_sequence`, the list of raw boxes, returned by `recognizer`, calculates mean width and height, thus we can know if the box is too large or too small. 

As long as some of the boxes may be double decker ones(containing letters from 2 rows), we have to preserve the order, that's why we can pass the matrix width into the normalizer, it will internally recreate the approximate matrix, split the double decker box, and save letter order that is close to the original(later it's possible to add the ability to pass the exact shape of the table). So the calculations wouldn't be too corrupted.

Finally the normalizer pads all the boxes to the exact same size (now it's 64x64) and returns the normalized letter sequence. 
The last part is the classification itself.

### Classification

For the final step I could probably use something like neural net, but I thought it would be an overkill for the 3-class classification. So I decided to use one of these models: [LogReg](http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html), [Random Forest](http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html), and [SVM](http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html). I chose the last one, because it has the most impressive results, according to some benchmarks. Again, I made another small [wrapper](https://github.com/alxrm/messy-letters-classifier/blob/master/model.py) for the model, so it's more straightforward to load the images and get the results from the trained model.

__It was pretty fun problem to solve, the workflow looks something like [this](https://github.com/alxrm/messy-letters-classifier/blob/master/scripts/eval.py)__

License
-------
    Copyright (c) 2017 Alexey Derbyshev

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.


