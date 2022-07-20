from app.process import makePrediction, processMultiSequence, crop, normalise
from app.plot import randomSlice
from app import model

import nibabel as nib
import numpy as np
import os
import sys

def testProcessMultiSequence():  
    if sys.platform == "win32":
        testingDir = os.listdir(r"tests\unit\testProcessFunctions\testingData\BraTS2021_00000")
        for file in testingDir:
            if "seg" in file:
                testingDir.remove(file)
        fileList = []
        for file in testingDir:
            fileList.append(os.path.join(r"tests\unit\testProcessFunctions\testingData\BraTS2021_00000", file))
    else:
        testingDir = os.listdir(r"tests/unit/testProcessFunctions/testingData/BraTS2021_00000")
        for file in testingDir:
            if "seg" in file:
                testingDir.remove(file)
        fileList = []
        for file in testingDir:
            fileList.append(os.path.join(r"tests/unit/testProcessFunctions/testingData/BraTS2021_00000", file))          
    testImage = processMultiSequence(fileList, testing=True)
    assert testImage.shape == (128,128,128,4)

def testProcessMultiSequenceWithEmptyFilelist():
    fileList = []
    testImage = processMultiSequence(fileList, testing=True)
    assert not testImage 

def testProcessMultiSequenceWithLargeFilelist():
    fileList = ["testPath1", "testPath2", "testPath3", "testPath4", "testPath5"]
    testImage = processMultiSequence(fileList, testing=True)
    assert not testImage 

def testCropImageFunction():
    testImage = nib.load("tests/unit/testProcessFunctions/testingData/BraTS2021_00000/BraTS2021_00000_flair.nii.gz").get_fdata()
    croppedImage = crop(testImage)
    assert croppedImage.shape == (128,128,128)

def testCropFunctionWithEmptyArray():
    testImage = np.zeros((240,240,155))
    croppedImage = crop(testImage)
    assert croppedImage.shape == (128,128,128)

def testRandomSliceFunction():
    testSlice = randomSlice()
    assert type(testSlice) == int
    assert testSlice >= 0 and testSlice <= 127 

def testNormalise():
    image = nib.load("tests/unit/testProcessFunctions/testingData/BraTS2021_00000/BraTS2021_00000_flair.nii.gz").get_fdata()
    image = normalise(image)
    assert image.min() == 0
    assert image.max() == 1

def testNormaliseWithInvalidShapeSmall():
    image = np.zeros((2,2))
    image = normalise(image)
    assert not image

def testNormaliseWithInvalidShapeLarge():
    image = np.zeros((5,5,5,5))
    image = normalise(image)
    assert not image

def testNormaliseWithSmallerDimensions():
    image = np.zeros((150,150,150))
    image = normalise(image)
    assert not image

def testNormaliseWithLargerDimensions():
    image = np.zeros((300,300,300))
    image = normalise(image)
    assert not image

def testMakePredictionFunctionWithRealImage():
    image = np.load("app/static/uploads/scans/0.npy")
    pred = makePrediction(image, model)
    assert pred.shape == (128,128,128)

def testMakePredictionFunctionWithEmptyImage():
    image = np.zeros((128,128,128,4))
    pred = makePrediction(image, model)
    assert pred.shape == (128,128,128)

def testMakePredictionWithInvalidImageShape():
    image = np.zeros((2,2))
    pred = makePrediction(image, model)
    assert not pred

    

