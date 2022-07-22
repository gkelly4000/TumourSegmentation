import nibabel as nib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

from tensorflow.keras import backend as K 
from werkzeug.utils import secure_filename

def normalise(image):
    """_summary_ Function to normalise an image's voxels to have a min of 0 and max of 1

    Args:
        image (np.array): Numpy array of a three dimensional image

    Returns:
       np.array: Numpy array containing the normalised image
    """
    if image.shape != (240,240,155):
        return False
    scaler = MinMaxScaler()
    scaledImage = scaler.fit_transform(image.reshape(-1, image.shape[-1])).reshape(image.shape)
    return scaledImage


def processMultiSequence(files, testing=False):
    """_summary_ Processes and normalises a set of mri images for one particular case

    Args:
        files (List):List of directories containing the images
        testing (boolean): Testing flag to tell function to remove images that are uploaded during unit tests

    Returns:
        np.array: Numpy array of the four MR sequences
    """
    if len(files) != 4:
        return False

    
    for i in range(len(files)):
        if "flair" in files[i].lower():
            flairImage = nib.load(files[i]).get_fdata()
        elif "t1ce" in files[i].lower():
            t1ceImage = nib.load(files[i]).get_fdata()
        elif "t1" in files[i].lower():
            t1Image = nib.load(files[i]).get_fdata()
        elif "t2" in files[i].lower():
            t2Image = nib.load(files[i]).get_fdata()
   

    scaledFlair = normalise(flairImage)
    scaledT1ce = normalise(t1ceImage)
    scaledT1 = normalise(t1Image)
    scaledT2 = normalise(t2Image)

    multiImg = np.stack([scaledFlair, scaledT1ce, scaledT1, scaledT2], axis=3)
    multiImg = crop(multiImg)
    return multiImg

def crop(image):
    """Function to crop an image to the size of 128x128x128

    Args:
        image (np.array): Numpy array of a MR image

    Returns:
        np.array: Cropped image 
    """
    height = image.shape[0]
    width = image.shape[1]
    depth = image.shape[2]

    hStart = int((height - 128) / 2)
    hEnd = int((height - (height - 128) / 2))

    wStart = int((width - 128) / 2)
    wEnd = int((width - (width - 128) / 2))

    dStart = int((depth - 128) / 2)
    dEnd = int((depth - (depth - 128) / 2))
    
    image = image[hStart:hEnd, wStart:wEnd, dStart:dEnd]
    return image

def makePrediction(image, model):
    """Function to make a prediction on a processed MR image

    Args:
        image (np.array): _description_
        model (tf.keras.Model): Model object for segmentation

    Returns:
        np.array: Prediction mask
    """
    if image.shape != (128,128,128,4):
        return False
    imageInput = np.expand_dims(image, axis=0)
    pred = model.predict(imageInput)
    predArgMax = np.argmax(pred, axis=4)[0,:,:,:]
    return predArgMax

def uploadProcessFiles(fileList):
    """Function to upload and save the MR images to temporary storage

    Args:
        fileList (List): List of uploaded files

    Returns:
        Function: Calls the function to process the uploaded files
    """
    files = []
    for file in fileList:
            fileName = secure_filename(file.filename)
            filePath = os.path.join('app/static/uploads/tmp', fileName)
            file.save(filePath)
            files.append(filePath)
    return processMultiSequence(files)

