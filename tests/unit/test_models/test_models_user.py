from app.models import User
from app import db
import pytest
from sqlalchemy.exc import IntegrityError

############################################################################
# TESTING USER MODEL
########################################################################
def testNewUser():
    """
    GIVEN a User model
    WHEN a new User is creates
    THEN chech the username, userEmail and hash userPassword is defined correctly
    """

    user = User(username="testNewUser1", userEmail="newUser1@email.com", userPassword="testPassword1")
    assert user.username == "testNewUser1"
    assert user.userEmail == "newUser1@email.com"
    assert user.userPassword != "testPassword1"

def testNewUserDuplicateEmail():
    """
    GIVEN a User model
    WHEN a new User is created with an email address already in the database
    THEN check that the new user is not created
    """
    db.drop_all()
    db.create_all()
    user = User(username="testNewUser1", userEmail="newUser1@email.com", userPassword="testPassword1")
    db.session.add(user)
    # db.session.commit()
    userWithDuplicateEmail = User(username="testNewUser2", userEmail="newUser1@email.com", userPassword="testPassword1")
    db.session.add(userWithDuplicateEmail)

    with pytest.raises(IntegrityError):
        db.session.commit()
    db.session.rollback()

def testNewUserDuplicateUsername():
    """
    GIVEN a User model
    WHEN a new User is created with a username already in the database
    THEN check that the new user is not created
    """
    
    db.drop_all()
    db.create_all()
    user = User(username="testNewUser1", userEmail="newUser1@email.com", userPassword="testPassword1")
    db.session.add(user)
    # db.session.commit()
    userWithDuplicateUsername = User(username="testNewUser1", userEmail="newUser2@email.com", userPassword="testPassword1")
    db.session.add(userWithDuplicateUsername)

    with pytest.raises(IntegrityError):
        db.session.commit()

    db.session.rollback()
    
    

def testNewUserWithPasswordLongerThanMaxLength():
    """
    GIVEN a User model
    WHEN a new User is created with a username already in the database
    THEN check that the new user is not created
    """
    db.drop_all()
    db.create_all()
    longPassword = "A"*81
    user = User(username="testNewUser1", userEmail="newUser1@email.com", userPassword=longPassword)
    db.session.add(user)
    assert not db.session.commit()
    db.session.rollback()
    # db.session.rollback()

def testUpdateUsername():
    db.drop_all()
    db.create_all()
    username="testNewUser1" 
    userEmail="newUser1@email.com" 
    userPassword="testPassword1"
    user1 = User(username=username, userEmail=userEmail, userPassword=userPassword)
    db.session.add(user1)
    db.session.commit()
    user1 = User.query.filter_by(username=username).first()
    testUpdateUsername = "testUpdateUsername"
    user1.username = testUpdateUsername
    db.session.commit()
    checkUpdateUser = User.query.filter_by(username=testUpdateUsername).first()
    assert checkUpdateUser.username == testUpdateUsername
    assert checkUpdateUser.username != username
    assert checkUpdateUser.userEmail == userEmail
    

    