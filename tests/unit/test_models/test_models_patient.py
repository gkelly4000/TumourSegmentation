from app.models import  Patient
from app import db
from datetime import date

def testNewPatient():

    newPatient = Patient(
        pName = "testPatient1",
        pDoB = "2000-01-01",
        pAddress = "Test Patient Address",
        pPostcode = "tp1tp1",
        pCity = "TestCity",
        pTelephone = "0117111222"
    )
    assert newPatient.pName == "testPatient1"
    assert newPatient.pDoB == "2000-01-01"
    assert newPatient.pAddress == "Test Patient Address"
    assert newPatient.pPostcode == "tp1tp1"
    assert newPatient.pCity == "TestCity"
    assert newPatient.pTelephone == "0117111222"

def testUpdatePatient():
    newPatient = Patient(
        pName = "testPatient1",
        pDoB = date(2020, 5, 17),
        pAddress = "Test Patient Address",
        pPostcode = "tp1tp1",
        pCity = "TestCity",
        pTelephone = "0117111222"
    )

    newPatient.pName = "testUpdatePatientName"
    newPatient.pDoB = "2001-01-01"
    newPatient.pAddress = "Updated Patient Address"
    newPatient.pPostcode = "utp11tp"
    newPatient.pCity = "UpdatedCity"
    newPatient.pTelephone = "0117999888"

    assert newPatient.pName == "testUpdatePatientName"
    assert newPatient.pDoB == "2001-01-01"
    assert newPatient.pAddress == "Updated Patient Address"
    assert newPatient.pPostcode == "utp11tp"
    assert newPatient.pCity == "UpdatedCity"
    assert newPatient.pTelephone == "0117999888"

def testUpdatePatientOnDatebase():
    db.drop_all()
    db.create_all()

    newPatient = Patient(
        pName = "testPatient1",
        pDoB = date(2020, 5, 17),
        pAddress = "Test Patient Address",
        pPostcode = "tp1tp1",
        pCity = "TestCity",
        pTelephone = "0117111222"
    )

    db.session.add(newPatient)
    db.session.commit()

    patient = Patient.query.filter_by(pName="testPatient1").first()
    patient.pName = "UpdatedName"

    db.session.commit()

    checkPatient = Patient.query.filter_by(pName="UpdatedName").first()

    assert checkPatient.pName == "UpdatedName"
    db.session.rollback()

def testDeletePatient():
    db.drop_all()
    db.create_all()

    newPatient = Patient(
        pName = "testPatient1",
        pDoB = date(2020, 5, 17),
        pAddress = "Test Patient Address",
        pPostcode = "tp1tp1",
        pCity = "TestCity",
        pTelephone = "0117111222"
    )
    db.session.add(newPatient)
    db.session.commit()

    Patient.query.filter_by(pName = "testPatient1").delete()

    results = Patient.query.filter_by(pName = "testPatient1")

    assert results.count() == 0
    db.session.rollback()

