from app.models import Doctor
from app import db

def testNewDoctor():

    newDoctor = Doctor(
        dName = "testDoctor1",
        dTele = "0117111222",
        dEmail = "test@doctor.com"
    )
    assert newDoctor.dName == "testDoctor1"
    assert newDoctor.dTele == "0117111222"
    assert newDoctor.dEmail == "test@doctor.com"

def testUpdateDoctor():
    newDoctor = Doctor(
        dName = "testDoctor1",
        dTele = "0117111222",
        dEmail = "test@doctor.com"
    )

    newDoctor.dName = "testUpdateDoctorName"
    newDoctor.dTele = "0117999888"
    newDoctor.dEmail = "test@doctor.com"

    assert newDoctor.dName == "testUpdateDoctorName"
    assert newDoctor.dTele == "0117999888"
    assert newDoctor.dEmail == "test@doctor.com"

def testUpdateDoctorOnDatebase():
    db.drop_all()
    db.create_all()

    newDoctor = Doctor(
        dName = "testDoctor1",
        dTele = "0117111222",
        dEmail = "test@doctor.com"
    )

    db.session.add(newDoctor)
    db.session.commit()

    doctor = Doctor.query.filter_by(dName="testDoctor1").first()
    doctor.dName = "UpdatedName"

    db.session.commit()

    checkDoctor = Doctor.query.filter_by(dName="UpdatedName").first()

    assert checkDoctor.dName == "UpdatedName"
    db.session.rollback()

def testDeleteDoctor():
    db.drop_all()
    db.create_all()

    newDoctor = Doctor(
        dName = "testDoctor1",
        dTele = "0117111222",
        dEmail = "test@doctor.com"
    )
    db.session.add(newDoctor)
    db.session.commit()

    Doctor.query.filter_by(dName = "testDoctor1").delete()

    results = Doctor.query.filter_by(dName = "testPatient1")

    assert results.count() == 0
    db.session.rollback()

