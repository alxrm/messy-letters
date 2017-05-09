# russian-letters-classifier
[![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)]()


Classification of strikethough/underlined/untouched letters from image


— so the task is __to count all underlined and strikethrough letters from the image__        
— okay, sounds cool, but what is the image?        
— well, it's gonna be something like [this](https://github.com/alxrm/messy-letters-classifier/blob/master/res/table_real.jpg)       
— so I have to cut all the letters out, know their positions, normalize the pictures of letters and then just feed them to the trained classifier

That's right, the repository is mostly about the last part of this "conversation", except it doesn't contain training datasets and trained model

For this task I've used SGD classifier, it seems to show the best results

For the rest, just take a look at the [eval.py](https://github.com/alxrm/messy-letters-classifier/blob/master/scripts/eval.py) 



