from app.models import User, Doctor, TestScan
from app import app, session, db
import json

def testLoginRouteGET():
    with app.test_client() as test_client:
        response = test_client.get("login")
        assert response.status_code == 200

def testLoginRoutePOST():
    with app.test_client() as test_client:
        response = test_client.post("/login", data={
        "username": "admin",
        "password": "rootroot",
        })
        assert response.status_code == 200

def testLoginRoutePOSTWrongCreds():
    with app.test_client() as test_client:
        response = test_client.put("/login")
        assert response.status_code != 200

def testLogoutRouteGET():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session["username"] = "admin"
            session["loggedIn"] = True
        response = test_client.get("/logout")
        assert response.status_code == 302

def testLogoutRoutePOST():
    with app.test_client() as test_client:
        with test_client.session_transaction() as session:
            session["username"] = "admin"
            session["loggedIn"] = True
        response = test_client.post("/logout")
        assert response.status_code == 405

def testRegisterRoutePOST():
    db.drop_all()
    db.create_all()
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = "admin"
            session["loggedIn"] = True
        response = test.post("/register", data= {
            "password": "testRegisterPassword",
            "username": "testRegisterUsername"
        })
        assert response.status_code == 302
    db.session.rollback()



def testRegisterRoutePOSTWithDatabase():
    db.drop_all()
    db.create_all()
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = "admin"
            session["loggedIn"] = True
        response = test.post("/register", data= {
            "password": "testRegisterPassword",
            "username": "testRegisterUsername",
            "email": "testRegister@email.com"
        })
        newUser = User.query.filter_by(username="testRegisterUsername").first()
        assert newUser
        assert newUser.username == "testRegisterUsername"
        assert newUser.userEmail == "testRegister@email.com"
        assert newUser.userPassword != "testRegisterPassword"
        db.session.rollback()

def testRegisterRouteGETAsAdmin():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = "admin"
            session["loggedIn"] = True
        response = test.get("/register")
        assert response.status_code == 200

def testRegisterRouteGETNotAdmin():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = "user"
            session["loggedIn"] = True
        response = test.get("/register")
        assert response.status_code == 302

def testRegisterRouteGETNotLoggedIn():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = None
            session["loggedIn"] = False
        response = test.get("/register")
        assert response.status_code == 302


def testViewPatientsGETLoggedIn():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = "user"
            session["loggedIn"] = True
        response= test.get("/viewPatients")
        assert response.status_code == 200

def testViewPatientsGETNotLoggedIn():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = None
            session["loggedIn"] = False
        response= test.get("/viewPatients")
        assert response.status_code == 302

def testViewPatientsPOST():
    with app.test_client() as test:
        response= test.post("/viewPatients")
        assert response.status_code == 405

def testViewPatientsPUT():
    with app.test_client() as test:
        response= test.put("/viewPatients")
        assert response.status_code == 405

def testViewTestsGET():
    with app.test_client() as test:
        response = test.get("/viewTests")
        assert response.status_code == 302


def testViewDoctorsPOST():
    with app.test_client() as test:
        response= test.post("/viewDoctors")
        assert response.status_code == 405

def testViewDoctorsPUT():
    with app.test_client() as test:
        response= test.put("/viewDoctors")
        assert response.status_code == 405



def testDisplayTestsGET():
    with app.test_client() as test:
        response = test.get("/displayTest", data = {
            "url": 'app/static/uploads/figures/fig.png',
            "buttonType": "test"
        })
        assert response.status_code == 200

def testDisplayTestPOST():
    with app.test_client() as test:
        response = test.post("/displayTest")
        assert response.status_code == 405

def testIndexPOSTLoggedIn():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = "user"
            session["loggedIn"] = True
        response = test.post("/")
        assert response.status_code == 405

def testIndexPOSTNotLoggedIn():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = None
            session["loggedIn"] = False
        response = test.post("/")
        assert response.status_code == 405

def testIndexGETLoggedIn():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = "user"
            session["loggedIn"] = True
        response = test.get("/")
        assert response.status_code == 302

def testIndexGETNotLoggedIn():
    with app.test_client() as test:
        with test.session_transaction() as session:
            session["username"] = None
            session["loggedIn"] = False
        response = test.get("/")
        assert response.status_code == 302

def testDisplayGET():
    with app.test_client() as test:
        response = test.get("/display")
        assert response.status_code == 405

def testDisplayPUT():
    with app.test_client() as test:
        response = test.put("/display")
        assert response.status_code == 405

def testDisplayImagesGET():
    with app.test_client() as test:
        response = test.get("/displayTest", data = {
            "url": 'app/static/uploads/figures/fig.png',
            "buttonType": "displayImages"
        })
        assert response.status_code == 200

def testDisplayImagesPOST():
    with app.test_client() as test:
        response = test.post("/displayTest", data = {
            "url": 'app/static/uploads/figures/fig.png',
            "buttonType": "displayImages"
        })
        assert response.status_code == 405
