from app.validators import validateUpload, validateSliceNum
import numpy as np

def testValidateUpload():
    testArray = np.load(r"app\static\uploads\scans\0.npy")
    assert validateUpload(testArray)

def testvalidateUploadWithEmptyArray():
    l = []
    testArray = np.array(l)
    assert not validateUpload(testArray)

def testValidateSliceNumWithValidNums():
    assert validateSliceNum(0)
    assert validateSliceNum(1)
    assert validateSliceNum(65)
    assert validateSliceNum(126)
    assert validateSliceNum(127)
    

def testValidateSliceNumAboveLimit():
    assert not validateSliceNum(128)
    assert not validateSliceNum(129)
    assert not validateSliceNum(130)

def testValidateSliceNumGreatlyAboveLimit():
    assert not validateSliceNum(1280000)
    assert not validateSliceNum(12800000)
    assert not validateSliceNum(128000000)
    

def testValidateSliceNumUnderLimit():
    assert not validateSliceNum(-1)
    assert not validateSliceNum(-2)
    assert not validateSliceNum(-5)
    assert not validateSliceNum(-10)

def testValidateSliceNumGreatlyUnderLimit():
    assert not validateSliceNum(-1000000)
    assert not validateSliceNum(-10000000)
    assert not validateSliceNum(-100000000)
    

def testValidateSliceNumWithString():
    testString = "testString"
    assert not validateSliceNum("testString")
    assert not validateSliceNum("testString"*2)
    assert not validateSliceNum("testString"*10)
    assert not validateSliceNum("testString"*100)

def testValidateSliceNumWithFloats():
    assert not validateSliceNum(0.)
    assert not validateSliceNum(1.)
    assert not validateSliceNum(65.)
    assert not validateSliceNum(126.)
    assert not validateSliceNum(127.)