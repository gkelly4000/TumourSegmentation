
def validateUpload(arr):
    """Validate new scan uploads to ensure they are the correct format and number of scans

    Args:
        arr (array): Array containing the the files to uplaod

    Returns:
        Boolean: Returns true if the upload has been validate correctly, false otherwise
    """
    if len(arr) != 4:
        return False
    for ele in arr:
        if ele.filename.split(".")[1] != "nii":
            return False
    return True


def validateMaskUpload(file):
    if file.filename.split(".")[1] != "nii":
        return False
    return True



def validateSliceNum(num):
    """Function to validate image slice number

    Args:
        num (integer): Integer between 0 and 127

    Returns:
        Boolean: Returns true if slice number is within the correct range, false otherwise.
    """
    if type(num) is not int:
        return False
    if num < 0 or num > 127:
        return False
    return True
