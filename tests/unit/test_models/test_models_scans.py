from app.models import Scan, Doctor, Patient
from app import db
from datetime import date

def testNewScan():
    newScan = Scan(
        sDateTime = date(2020, 5, 17),
        sModality = "MultiSequence",
        sImage = r"app\static\uploads\scans\0.npy"
    )
    assert newScan.sDateTime == date(2020, 5, 17)
    assert newScan.sModality == "MultiSequence"
    assert newScan.sImage == r"app\static\uploads\scans\0.npy"

def testNewScanDatabase():
    db.drop_all()
    db.create_all()
    newScan = Scan(
        sDateTime = date(2020, 5, 17),
        sModality = "MultiSequence",
        sImage = r"app\static\uploads\scans\0.npy"
    )
    db.session.add(newScan)
    db.session.commit()
    scanToCheck =Scan.query.filter_by(sImage = r"app\static\uploads\scans\0.npy").first()
    assert scanToCheck.sDateTime == date(2020, 5, 17)
    assert scanToCheck.sModality == "MultiSequence"
    assert scanToCheck.sImage == r"app\static\uploads\scans\0.npy"
    db.session.rollback()

def testScanForiegnKeys():
    db.drop_all()
    db.create_all()

    newDoctor = Doctor(
        dName = "testDoctor1",
        dTele = "0117111222",
        dEmail = "test@doctor.com"
    )

    newPatient = Patient(
        pName = "testPatient1",
        pDoB = date(2020, 5, 17),
        pAddress = "Test Patient Address",
        pPostcode = "tp1tp1",
        pCity = "TestCity",
        pTelephone = "0117111222"
    )
    db.session.add(newDoctor)
    db.session.add(newPatient)
    db.session.commit()

    fkPatient = Patient.query.filter_by(pName = "testPatient1").first()
    fkPatientID = fkPatient.pID

    fkDoctor = Doctor.query.filter_by(dName="testDoctor1").first()
    fkDoctorID = fkDoctor.dID
    newScan = Scan(
        sDateTime = date(2020, 5, 17),
        sModality = "MultiSequence",
        sImage = r"app\static\uploads\scans\0.npy",
        patientID = fkPatientID,
        doctorID = fkDoctorID
    )

    db.session.add(newScan)
    db.session.commit()
    scanToCheck =Scan.query.filter_by(sImage = r"app\static\uploads\scans\0.npy").first()
    assert scanToCheck.patientID == fkPatientID
    assert scanToCheck.doctorID == fkDoctorID
    
