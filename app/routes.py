from app.models import User, Patient, Doctor, Scan, TestScan
from app.process import uploadProcessFiles, makePrediction, crop
from app.forms import RegisterDoctorForm, RegisterPatientForm, RegisterUserForm, UploadScanForm, UploadTestScanForm, LoginForm
from app.auth import isLoggedIn, checkAdmin
from app.validators import validateUpload,validateSliceNum, validateMaskUpload
from app.setters import setSessionDefaults
from app.plot import visualisePrediction, visualise, visualiseTest
from app.metrics import dice_coef_multilabel, getIoU

import numpy as np
import nibabel as nib
import hashlib
import os

from flask import render_template,request, redirect, url_for, session, flash
# from tensorflow.keras.utils import to_categorical
from werkzeug.utils import secure_filename

from app import app, model, db, process, admin

def setImageGlobal(image):
    global IMAGE
    IMAGE = image

def setPredGlobal(pred):
    global PRED
    PRED = pred

def setMaskGlobal(mask):
    global MASK
    MASK = mask

@app.route("/logout")
def logout():
    """_summary_

    Returns:
        _type_: _description_
    """
    
    user = session["username"]
    if user:
        session["loggedIn"] = False
        session["username"] = None
        flash(f"Successfully logged out user: {user}","success")
    else:
        flash("No user to log out.", "danger")
    return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    """Function that logs a user in

    Returns:
       render(HTML) Renders the listImage.html page on suvvessful login, otherwise returns the loging form and page again.
    """
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password = form.password.data
        hashedPassword = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if hashedPassword == user.userPassword:
                session['loggedIn'] = True
                session['username'] = username
                flash(f"Successfully logged in user: {username}", "success")
                return redirect(url_for("list"))
            flash("Invalid username or password. Please try again.", "danger")
        else:
            flash("Invalid username or password. Please try again.", "danger")
        return render_template("login.html", form=form)
    return render_template("login.html",form=form)

@app.route("/register", methods=["POST", "GET"])
def register():
    """_summary_

    Returns:
        _type_: _description_
    """
    
    if not checkAdmin():
        flash("Only adminstrators can register new users", "danger")
        if isLoggedIn():
            return redirect(url_for("list"))
        else:
            return redirect(url_for("login"))

    form = RegisterUserForm(request.form)
    if request.method == "POST":
        password = form.password.data
        username =  form.username.data

        email = form.email.data
        # hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        newUser = User(username=username, userEmail=email, userPassword=password)
        db.session.add(newUser)
        db.session.commit()
        flash("New user created! Please log in. ", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/deleteDoctor", methods=['POST'])
def deleteDoctor():
    """_summary_

    Returns:
        _type_: _description_
    """
    if checkAdmin():
        selectedID = request.form.get("doctorChoice")
        Doctor.query.filter_by(dID=selectedID).delete()
        db.session.commit()
        flash("Doctor Record Deleted", "success")
        return redirect(url_for("viewDoctors"))
    else:
        flash("Only adminstrators can access this page", "danger")
        return viewDoctors()

@app.route("/viewDoctors")
def viewDoctors():
    if not isLoggedIn():
        flash("Only authenticated user can access doctor details", "danger")
        return redirect(url_for("login"))
    doctors = Doctor.query.all()
    return render_template("viewDoctors.html", context=doctors)

@app.route("/deletePatient", methods=['POST'])
def deletePatient():
    if not isLoggedIn():
        flash("Only authenticated users can delete records", "danger")
        return viewPatients()
    selectedID = request.form.get("patientChoice")
    Patient.query.filter_by(pID=selectedID).delete()
    db.session.commit()
    return render_template("home.html")

@app.route("/deleteScan", methods=['POST'])
def deleteScan():
    if not isLoggedIn():
        flash("Only authenticated users can delete patient scans", "danger")
        return redirect(url_for("list"))
    selectedID = request.form.get("choice")
    Scan.query.filter_by(sID=selectedID).delete()
    db.session.commit()
    return redirect(url_for("list"))

@app.route("/deleteTestScan", methods=['POST'])
def deleteTestScan():
    if not isLoggedIn():
        flash("Only authenticated users can delete test scans", "danger")
        return redirect(url_for("viewTest"))
    selectedID = request.form.get("tChoice")
    TestScan.query.filter_by(tID=selectedID).delete()
    db.session.commit()
    return redirect(url_for("viewTests"))

@app.route("/viewPatients")
def viewPatients():
    if not isLoggedIn():
        flash("Only authenticated users can view patient details", "danger")
        return redirect(url_for("login"))
    patients = Patient.query.all()
    return render_template("viewPatients.html", context=patients)

@app.route('/viewTests', methods=['GET', 'POST'])
def viewTests():
    if request.method == 'POST':
        selectedID = request.form.get("tChoice")
        data = TestScan.query.filter_by(tID=selectedID).first()
        imagePath = data.tImage
        maskPath = data.tMask

        npImage = np.load(imagePath)
        npMask = np.load(maskPath)

        pred = makePrediction(npImage, model)

        setImageGlobal(npImage)
        setMaskGlobal(npMask)
        setPredGlobal(pred)
        
        visualiseTest(IMAGE, MASK, PRED)
        flash(f"Mean IoU score for the image = {str(getIoU(MASK, PRED))}, Mean Dice Coefficient = {str(dice_coef_multilabel(MASK, PRED, numLabels=4))}","info")
        return redirect(url_for("displayTest"))
        
    tests = TestScan.query.all()
    if len(tests) == 0:
        flash("No test images exist, please upload new image and ground truth for testing.", "info")
        return redirect(url_for("test"))
    return render_template("viewTests.html", context=tests)

@app.route("/displayTest")
def displayTest():
    args = {
    "url": 'app/static/uploads/figures/fig.png',
    "buttonType": "test"
    }
    return render_template("display.html",context=args)

@app.route("/getRandomTestSlice")
def getRandomTestSlice():
    visualiseTest(IMAGE, MASK, PRED, isRan=True)
    return redirect(url_for("displayTest"))

@app.route("/getTestSlice")
def getTestSlice():
    sliceNum = int(request.args.get("sliceNum"))
    if validateSliceNum(sliceNum):
        visualiseTest(IMAGE, MASK, PRED, n=sliceNum)
    else:
        flash("Error: Out of range slice number (0-127)","danger")
    return redirect(url_for("displayTest"))

@app.route('/test', methods=['POST', 'GET'])
def test():
    if not isLoggedIn():
        flash("Only authenticated users can upload new scans for testing", "danger")
        return redirect(url_for("login"))

    form = UploadTestScanForm(request.form)
    if request.method == 'POST':
        imageList = request.files.getlist("testImage")
        if not validateUpload(imageList):
            flash("Error: Please select four sequences in NifTi format (Flair, T1, T1CE, T2)", 'danger')
            return redirect(url_for( "test"))

        multiSequenceImage = uploadProcessFiles(imageList)
        
        saveNum = str(len(os.listdir("app/static/uploads/testScans/image")))
        imagePath = os.path.join("app/static/uploads/testScans/image", saveNum + ".npy")
        maskPath = os.path.join("app/static/uploads/testScans/mask", saveNum + ".npy")
      
        np.save(imagePath, multiSequenceImage)

        maskFile = request.files['testMask']
        if not validateMaskUpload(maskFile):
            flash("Error: Segmentation mask must be in Nifti format", "danger")
            return redirect(url_for( "test"))
        maskFilePath = os.path.join('app/static/uploads/tmp', secure_filename(maskFile.filename))
        maskFile.save(maskFilePath)

        testMask = nib.load(maskFilePath).get_fdata()
        testMask[testMask==4] = 3
        testMask = crop(testMask)
        np.save(maskPath, testMask)

        newTest = TestScan(tImage=imagePath, tMask=maskPath)
        db.session.add(newTest)
        
        db.session.commit()
        return redirect(url_for("viewTests"))
    return render_template("test.html", form=form)

@app.route('/')
def index():
    try:
        if isLoggedIn():
            return redirect(url_for("list"))
        else:
            return redirect(url_for("login"))
    except:
        setSessionDefaults()
        return redirect(url_for("index"))

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if not isLoggedIn():
        flash("Please log in to upload a new scan to processing", "danger")
        return redirect(url_for("login"))
    form = UploadScanForm(request.form)
    if request.method == 'POST':
        imageList = request.files.getlist("image")

        if not validateUpload(imageList):
            flash("Error: Please select four sequences (Flair, T1, T1CE, T2) in Nifti format", "danger")
            return redirect(url_for("list")) 


        multiSequenceImage = uploadProcessFiles(imageList)
        
        imagePath = os.path.join("app/static/uploads/scans", str(len(os.listdir("app/static/uploads/scans")))+".npy")
        np.save(imagePath, multiSequenceImage)

        newScan = Scan(sDateTime=form.scanDateTime.data, sModality=form.modality.data, sImage=imagePath, patientID=form.patientID.data, doctorID=form.doctorID.data)
        db.session.add(newScan)
        db.session.commit()
        return redirect(url_for("list")) 
    return render_template("upload.html", form=form)

@app.route('/list', methods=['POST','GET'])
def list():
    if isLoggedIn():
        if request.method == 'POST':
            choice = request.form.get("filterChoice")
            scans = Scan.query.filter_by(patientID=choice)
            return render_template("listImages.html", context=scans)
        else: 
            scans = Scan.query.all()
            return render_template("listImages.html", context=scans)
    else:
        flash("Only authenticated users can access patient scans, please log or use the testing scans", "danger")
        return redirect(url_for("login"))

@app.route("/display", methods=['POST'])
def display():
    if request.method == 'POST':
        args = {
            "url": 'app/static/uploads/figures/fig.png',
            "buttonType": "displayImages"
        }
        selectedImageID = request.form.get("choice")
        data = Scan.query.filter_by(sID=selectedImageID).first()
        imagePath = data.sImage
        npImage = np.load(imagePath)        

        setImageGlobal(npImage)
        visualise(npImage)
        return redirect(url_for("displayImages"))

@app.route("/displayImages")
def displayImages():
    args = {
            "url": 'app/static/uploads/figures/fig.png',
            "buttonType": "displayImages"
        }
    return render_template("display.html",context=args)

@app.route("/getRandomSlice")
def getRandomSlice():
    visualise(IMAGE, isRan=True)
    return redirect(url_for("displayImages"))

@app.route("/getSlice")
def getSlice():
    sliceNum = int(request.args.get("sliceNum"))
    if validateSliceNum(sliceNum):
        visualise(IMAGE, n=sliceNum)
    else:
        flash("Error: Out of range slice number (0-127)","danger")
    return redirect(url_for("displayImages"))

@app.route("/displayPrediction")
def displayPrediction():
    args = {
        "url": "app/static/uploads/figures/fig.png",
        "buttonType": "prediction"
    }
    return render_template("display.html", context=args)

@app.route("/getRandomPredSlice")
def getRandomPredSlice():
    visualisePrediction(IMAGE, PRED, isRan=True)
    return redirect(url_for("displayPrediction"))

@app.route("/getPredSlice")
def getPredSlice():
    sliceNum = int(request.args.get("sliceNum"))
    if validateSliceNum(sliceNum):
        visualisePrediction(IMAGE, PRED, n=sliceNum)
    else:
        flash("Error: Out of range slice number (0-127)")
    return redirect(url_for("displayPrediction"))

@app.route('/predict/visualise', methods=['POST', 'GET'])
def makeAndDisplayPred(image, prediction, isRandom=False):
    if request.method == "POST" or request.method == "GET":
        visualisePrediction(image, prediction)
        return redirect(url_for("displayPrediction"))

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        selectedImageID = request.form.get("choice")
        data = Scan.query.filter_by(sID=selectedImageID).first()
        imagePath = data.sImage
        npImage = np.load(imagePath)
        prediction = makePrediction(npImage, model)
        setImageGlobal(npImage)
        setPredGlobal(prediction)
        return makeAndDisplayPred(IMAGE, PRED)

@app.route('/registerPatient', methods=['GET','POST'])
def registerPatient():
    if not isLoggedIn():
        flash("Only authenticated users can register patients", "danger")
        return redirect(url_for("login"))
    form = RegisterPatientForm(request.form)
    if request.method == 'POST':
        newPatient = Patient(
            pName=form.patientName.data, 
            pDoB=form.dob.data,pAddress=form.address.data, 
            pPostcode=form.postcode.data,pCity=form.city.data, 
            pTelephone=form.telephone.data
        )
        db.session.add(newPatient)
        db.session.commit()
        return redirect(url_for("list"))
    return render_template("registerPatient.html", form=form)

@app.route("/registerDoctor", methods=['POST', 'GET'])
def registerDoctor():
    if not isLoggedIn():
        flash("Only authenticated users can register doctors", "danger")
        return redirect(url_for("login"))
    form = RegisterDoctorForm(request.form)
    if request.method == 'POST':
        newDoctor = Doctor(
            dName=form.doctorName.data, 
            dTele=form.doctorTelephone.data,
            dEmail=form.doctorEmail.data
        )
        db.session.add(newDoctor)
        db.session.commit()
        return redirect(url_for("list"))
    return render_template("registerDoctor.html", form=form)

@app.route("/displayScanContactDetails", methods=['POST'])
def displayScanContactDetails():
    if not isLoggedIn():
        flash("Only authenicated users can access contact details", "danger")
        return redirect(url_for("login"))
    if request.method == 'POST':
        selectedImageID = request.form.get("choice")
        data = Scan.query.filter_by(sID=selectedImageID).first()
        patientID = data.patientID
        patientData = Patient.query.filter_by(pID = patientID).first()
        doctorID = data.doctorID
        doctorData = Doctor.query.filter_by(dID = doctorID).first()
        # dob = Scan.query(distinct(func.date_part("YEAR", Scan)))
        context = {
            "doctor": doctorData,
            "patient": patientData
        }
        return render_template("displayScanContactDetails.html", context=context)