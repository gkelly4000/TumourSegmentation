from flask import session

def setSessionDefaults():
    session["loggedIn"] = False
    session["username"] = None

