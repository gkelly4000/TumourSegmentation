import numpy as np

from keras.metrics import MeanIoU
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K 


def dice_coef(y_true, y_pred):
    """_summary_
    Adapted from: https://stackoverflow.com/questions/61488732/how-calculate-the-dice-coefficient-for-multi-class-segmentation-task-using-pytho

    Args:
        y_true (_type_): _description_
        y_pred (_type_): _description_

    Returns:
        _type_: _description_
    """
    y_true_f = y_true.flatten()
    y_pred_f = y_pred.flatten()
    intersection = np.sum(y_true_f * y_pred_f)
    smooth = 0.0001
    return (2. * intersection + smooth) / (np.sum(y_true_f) + np.sum(y_pred_f) + smooth)

def dice_coef_multilabel(y_true, y_pred, numLabels):
    """_summary_
    Adapted from: https://stackoverflow.com/questions/61488732/how-calculate-the-dice-coefficient-for-multi-class-segmentation-task-using-pytho

    Args:
        y_true (_type_): _description_
        y_pred (_type_): _description_
        numLabels (_type_): _description_

    Returns:
        _type_: _description_
    """
    if y_true.shape != (128,128,128) or y_pred.shape != (128,128,128):
        return False
    y_true = to_categorical(y_true, num_classes=numLabels)
    y_pred = to_categorical(y_pred, num_classes=numLabels)
    dice=0
    for index in range(numLabels):
        dice += dice_coef(y_true[:,:,:,index], y_pred[:,:,:,index])
    return dice/numLabels 
    
def getIoU(pred, mask):
    """
        Function to calculate the Intersection over Union score for a 
        predicted image and the corresponding ground truth

    Args:
        pred (npArray): Prediction array in the shape (128,128,128) 
        mask (_type_): Ground truth array in the shape (128,128,128)

    Returns:
        npArray: The calculated IoU score between the prediction array and ground truth array
    """
    if pred.shape != (128,128,128) or mask.shape != (128,128,128):
        return False
    mask = to_categorical(mask, num_classes=4)
    pred = to_categorical(pred, num_classes=4)
    nClass = 4
    iouScore = MeanIoU(num_classes=nClass)
    iouScore.update_state(pred, mask)
   
    return iouScore.result().numpy()