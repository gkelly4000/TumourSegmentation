import matplotlib.pyplot as plt
import random

def randomSlice():
    return random.randint(0,127)

def visualisePrediction(image, prediction,numRows=3,numCols=2, isRan=False, n=69):

    if isRan:
        n = randomSlice()
    print(n)
    
    #FLIAR CORNONAL
    plt.subplot(numRows,numCols,1)
    plt.imshow(image[:, n,:, 0], cmap="gray")
    plt.ylabel("Coronal")
    plt.title("Flair",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows,numCols,2)
    plt.imshow(prediction[:,n,:])
    plt.title("Prediction",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    #T1C2 TRANS
    plt.subplot(numRows,numCols,3)
    plt.imshow(image[:,:, n, 1], cmap="gray")
    plt.ylabel("Transversal")
    plt.title("T1CE",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows,numCols,4)
    plt.imshow(prediction[:,:,n])
    plt.title("Prediction",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    #T2 SAG
    plt.subplot(numRows,numCols,5)
    plt.imshow(image[n,:, :, 3], cmap="gray")
    plt.ylabel("Sagital")
    plt.title("T2",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows,numCols,6)
    plt.imshow(prediction[n,:,:])
    plt.title("Prediction",fontsize=8)
    plt.yticks([])
    plt.xticks([])
    
    plt.savefig("app/static/uploads/figures/fig.png")



def visualise(image, isRan=False, n=69):
    if isRan:
        n = random.randint(0,127)

    # Flair
    plt.subplot(4,3,1)
    plt.imshow(image[:, n,:, 0], cmap="gray")
    plt.yticks([])
    plt.xticks([])
    plt.ylabel("Flair")
    plt.title("Coronal")

    plt.subplot(4,3,2)
    plt.imshow(image[n,:,:,0], cmap="gray")
    plt.yticks([])
    plt.xticks([])
    plt.title("Sagitatl")

    plt.subplot(4,3,3)
    plt.imshow(image[:,:,n,0], cmap="gray")
    plt.yticks([])
    plt.xticks([])
    plt.title("Transveral")


    #T1CE

    plt.subplot(4,3,4)
    plt.imshow(image[:, n,:, 1], cmap="gray")
    plt.yticks([])
    plt.xticks([])
    plt.ylabel("T1CE")

    plt.subplot(4,3,5)
    plt.imshow(image[n,:,:,1], cmap="gray")
    plt.yticks([])
    plt.xticks([])

    plt.subplot(4,3,6)
    plt.imshow(image[:,:,n,1], cmap="gray")
    plt.yticks([])
    plt.xticks([])

    #T1
    plt.subplot(4,3,7)
    plt.imshow(image[:, n,:, 2], cmap="gray")
    plt.yticks([])
    plt.xticks([])
    plt.ylabel("T1")

    plt.subplot(4,3,8)
    plt.imshow(image[n,:,:,2], cmap="gray")
    plt.yticks([])
    plt.xticks([])

    plt.subplot(4,3,9)
    plt.imshow(image[:,:,n,2], cmap="gray")
    plt.yticks([])
    plt.xticks([])

    #T2
    plt.subplot(4,3,10)
    plt.imshow(image[:, n,:, 3], cmap="gray")
    plt.yticks([])
    plt.xticks([])
    plt.ylabel("T2")

    plt.subplot(4,3,11)
    plt.imshow(image[n,:,:,3], cmap="gray")
    plt.yticks([])
    plt.xticks([])

    plt.subplot(4,3,12)
    plt.imshow(image[:,:,n,3], cmap="gray")
    plt.yticks([])  
    plt.xticks([])

    plt.savefig("app/static/uploads/figures/fig.png")

# def visualiseTest(image, mask, pred, numRows=3, numCols=5, n=69, isRan=False):

#     if isRan:
#         n = random.randint(0, 127)
    

#     #FLIAR CORNONAL
#     plt.subplot(numRows,numCols,1)
#     plt.imshow(image[:, n,:, 0], cmap="gray")
#     plt.ylabel("Coronal")
#     plt.title("Flair",fontsize=8)
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,2)
#     plt.imshow(image[:, n,:, 1], cmap="gray")
#     plt.ylabel("Coronal")
#     plt.title("T1CE",fontsize=8)
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,3)
#     plt.imshow(image[:, n,:, 2], cmap="gray")
#     plt.ylabel("Coronal")
#     plt.title("T1",fontsize=8)
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,4)
#     plt.imshow(image[:, n,:, 3], cmap="gray")
#     plt.ylabel("Coronal")
#     plt.title("T2",fontsize=8)
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,5)
#     plt.imshow(mask[:, n,:], cmap="gray")
#     plt.ylabel("Coronal")
#     plt.title("Ground Truth",fontsize=8)
#     plt.yticks([])
#     plt.xticks([])

#     #T1C2 TRANS
#     plt.subplot(numRows,numCols,6)
#     plt.imshow(image[:,:, n, 0], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,7)
#     plt.imshow(image[:,:, n, 1], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,8)
#     plt.imshow(image[:,:, n, 2], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,9)
#     plt.imshow(image[:,:, n, 3], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,10)
#     plt.imshow(mask[:, :,n], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

    

#     plt.subplot(numRows,numCols,11)
#     plt.imshow(image[n,:, :, 0], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,12)
#     plt.imshow(image[n,:, :, 1], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,13)
#     plt.imshow(image[n,:, :, 2], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,14)
#     plt.imshow(image[n,:, :, 3], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

#     plt.subplot(numRows,numCols,15)
#     plt.imshow(mask[n, :,:], cmap="gray")
#     plt.yticks([])
#     plt.xticks([])

   
    
#     plt.savefig("app/static/uploads/figures/fig.png")

def visualiseTest(image, mask, pred, numRows=3, numCols=3, n=69, isRan=False):

    if isRan:
        n = random.randint(0, 127)
    

    #FLIAR CORNONAL
    plt.subplot(numRows,numCols,1)
    plt.imshow(image[:, n,:, 0], cmap="gray")
    plt.ylabel("Coronal")
    plt.title("Flair",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows, numCols, 2)
    plt.imshow(mask[:,n,:])
    plt.title("Grond Truth",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows,numCols,3)
    plt.imshow(pred[:,n,:])
    plt.title("Prediction",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    #T1C2 TRANS
    plt.subplot(numRows,numCols,4)
    plt.imshow(image[:,:, n, 1], cmap="gray")
    plt.ylabel("Transversal")
    plt.title("T1CE",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows, numCols, 5)
    plt.imshow(mask[:,:,n])
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows, numCols, 6)
    plt.imshow(pred[:,:,n])
    plt.yticks([])
    plt.xticks([])


    #T2 SAG
    plt.subplot(numRows,numCols,7)
    plt.imshow(image[n,:, :, 3], cmap="gray")
    plt.ylabel("Sagital")
    plt.title("T2",fontsize=8)
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows, numCols, 8)
    plt.imshow(mask[n,:,:])
    plt.yticks([])
    plt.xticks([])

    plt.subplot(numRows, numCols, 9)
    plt.imshow(pred[n,:,:])
    plt.yticks([])
    plt.xticks([])
    
    plt.savefig("app/static/uploads/figures/fig.png")