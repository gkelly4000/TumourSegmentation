from flask import session
def checkAdmin():
    if isLoggedIn() and session["username"] == "admin":
        return True
    return False

def isLoggedIn():
    if session['loggedIn'] == True:
        return True
    return False