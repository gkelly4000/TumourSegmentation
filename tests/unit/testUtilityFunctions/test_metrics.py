from app.metrics import dice_coef, dice_coef_multilabel, getIoU
from app.process import makePrediction
from app import model
import numpy as np
from tensorflow.keras.utils import to_categorical

def testIoUWithRealImages():
    image = np.load("app/static/uploads/testScans/image/0.npy")
    mask = np.load("app/static/uploads/testScans/mask/0.npy")
    pred = makePrediction(image, model)
    iou = getIoU(pred, mask)
    assert iou.dtype == np.float32
    assert iou >= 0 and iou <= 1

def testIoUWithEmptyImages():
    testPred = np.zeros((128,128,128))
    testMask = np.zeros((128,128,128))
    iou = getIoU(testPred,testMask)
    assert iou.dtype == np.float32
    assert iou >= 0 and iou <= 1

def testIoUInvalidPredictionShape():
    testPred = np.zeros((128,128))
    testMask = np.zeros((128,128,128))
    iou = getIoU(testPred,testMask)
    assert not iou

def testIoUInvalidMaskShape():
    testPred = np.zeros((128,128,128))
    testMask = np.zeros((128,128))
    iou = getIoU(testPred,testMask)
    assert not iou

def testDiceCoefMultilabel():
    image = np.load("app/static/uploads/testScans/image/0.npy")
    mask = np.load("app/static/uploads/testScans/mask/0.npy")
    pred = makePrediction(image, model)
    multiDice = dice_coef_multilabel(mask, pred, numLabels=4)
    assert multiDice.dtype == np.float64
    assert multiDice >= 0 and multiDice <= 1

def testDiceCoefMultilabelInvalidPredictionShape():
    testPred = np.zeros((128,128))
    testMask = np.zeros((128,128,128))
    multiDice = dice_coef_multilabel(testMask, testPred, numLabels=4)
    assert not multiDice

def testDiceCoefMultilabelInvalidMaskShape():
    testMask = np.zeros((128,128))
    testPred = np.zeros((128,128,128))
    multiDice = dice_coef_multilabel(testMask, testPred, numLabels=4)
    assert not multiDice

def testSingleClassDiceCoef():
    image = np.load("app/static/uploads/testScans/image/0.npy")
    mask = np.load("app/static/uploads/testScans/mask/0.npy")
    pred = makePrediction(image, model)
    numClasses = 4
    mask = to_categorical(mask, num_classes=numClasses)
    pred = to_categorical(pred, num_classes=numClasses)
    for i in range(numClasses):
        dice = dice_coef(mask[:,:,:,i], pred[:,:,:,i])
        assert dice.dtype == np.float64
        assert dice >= 0 and dice <= 1