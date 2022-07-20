Brain Tumour Segmentation Application



<<WEB APPLICATION>>
    To install required libraries:
        pip3 install -r requirements.txt

    To run the web application on local host:
        python3 run.py 

    To Log in to the web application:
        Two accounts already exist for ease of use, a regular and admin account.
        To create new accounts, or database management, please log in as admin.

        Regular: username = gkelly4000, password = 12341234
        Admin: username = admin, password = rootroot

    Data:
        A subset of the dataset has been included in this repository, due to the size and number of images only a small subset has been included for ease of use.
        The full dataset can be downloaded from:
            https://www.kaggle.com/datasets/dschettler8845/brats-2021-task1

<<DOCKER>>
    To pull and run docker image from dockerhub:
        docker run grskelly/tumour-segmentation-application
        Go to: http://172.17.0.2:5000
