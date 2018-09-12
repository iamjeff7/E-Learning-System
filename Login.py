#!/usr/bin/python3
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore
import sys
from StudentProfile import *

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time

cred = credentials.Certificate('./ServiceAccountKey.json')
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

class Login(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Login Page"
        self.width = 450
        self.height = 800
        self.top = 100
        self.left = self.width/2
        
        # Global variables
        self.i = 1
        self.usersDict = {}
        self.tab = "login"

        #*****************************************************
        """self.stylesheet = 
            .self.loginTab{
                background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FBC2EB,stop: 1 #A6C1EE);
                border-radius: 115px;
                color: #FFFFFF;
            }

            QLabel{
                font-size: 23px;
            }
        """
        self.InitWindow()
        #self.setStyleSheet(self.stylesheet)

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.screenSize = QtWidgets.QDesktopWidget().screenGeometry(-1)
        #self.window.setGeometry(self.left, self.top, self.screenSize.width(), self.screenSize.height())
        self.setGeometry((self.screenSize.width()/2)-self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        # Set window background color
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)
        self.addComponents()
        self.show()

    def addComponents(self):
        loginLbl = QLabel("E-Learning System", self)
        loginLbl.setFixedHeight(100)
        loginLbl.setStyleSheet("QLabel{font-size: 23px}")
        #*******************************************************************************
        # Coordinates
        # ====
        self.top = 100
        self.loginLbl_X = self.left-90
        self.loginLbl_Y = 70+self.top
        self.userLE_X = self.left-100
        self.userLE_Y =200+self.top
        self.passLE_X =self.left-100
        self.passLE_Y =240+self.top
        '''self.ULELbl_X =
        self.ULELbl_Y = 
        self.PLELbl_X =
        self.PLELbl_Y =
        self.LoginTab_X =
        self.LoginTab_Y = 
        self.SignUpTab_X =
        self.SignUpTab_Y =
        self.loginBtn_X =
        self.LoginBtn_Y =
        self.siginBtn_X =
        self.siginBtn_Y =
        self.readBtn_X =
        self.readBtn_Y ='''
        #*******************************************************************************
        loginLbl.move(self.loginLbl_X,self.loginLbl_Y)
        self.userLE = QLineEdit(self)
        self.userLE.setPlaceholderText("  username")
        self.userLE.resize(200, 26)
        self.userLE.move(self.userLE_X,self.userLE_Y)
        self.passLE = QLineEdit(self)
        self.passLE.setPlaceholderText("  password")
        self.passLE.resize(200, 26)
        self.passLE.move(self.passLE_X,self.passLE_Y)
        self.passLE.setEchoMode(QLineEdit.Password)
        
        # ULELbl = User Login Error Label
        self.ULELbl = QLabel("not found!", self)
        self.ULELbl.setStyleSheet("QLabel{color: #FF0000}")
        self.ULELbl.move(9999,9999)

        # PLELbl = Password Login Error Label
        self.PLELbl = QLabel("incorrect!", self)
        self.PLELbl.setStyleSheet("QLabel{color: #FF0000}")
        self.PLELbl.move(9999,9999)

        self.LoginTab = QPushButton("Login", self)
        self.LoginTab.move(self.left-100, 150+self.top)
        self.LoginTab.resize(100,36)
        self.LoginTab.setStyleSheet("QPushButton{background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FBC2EB,stop: 1 #A6C1EE)}"
                                    "QPushButton{border-radius: 115px}"
                                    "QPushButton{color: #FFFFFF}")
        self.LoginTab.clicked.connect(self.LoginTabClicked)

        self.SignUpTab = QPushButton("Sign up", self)
        self.SignUpTab.move(self.left, 150+self.top)
        self.SignUpTab.resize(100,36)
        self.SignUpTab.setStyleSheet("QPushButton{background-color: white}"
                                     "QPushButton{border-radius: 115px}"
                                     "QPushButton{color: #8e838e}")
        self.SignUpTab.clicked.connect(self.SignUpTabClicked)

        self.loginBtn = QPushButton("Log in",self)
        self.loginBtn.move(self.left-100, 280+self.top)
        self.loginBtn.resize(200,36)
        self.loginBtn.clicked.connect(self.LoginClicked)
        self.loginBtn.setStyleSheet("QPushButton{background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FBC2EB,stop: 1 #A6C1EE)}"
                                    "QPushButton{border-radius: 115px}"
                                    "QPushButton{color: #FFFFFF}")

        self.readBtn = QPushButton("Read", self)
        self.readBtn.move(self.left-100, 320+self.top)
        self.readBtn.resize(200,36)
        self.readBtn.clicked.connect(self.ReadClicked)
        self.readBtn.setVisible(False)

        self.signupBtn = QPushButton("Sign up",self)
        self.signupBtn.move(9999,9999)
        self.signupBtn.resize(200,36)
        self.signupBtn.clicked.connect(self.SignUpClicked)
        self.signupBtn.setStyleSheet("QPushButton{background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FBC2EB,stop: 1 #A6C1EE)}"
                                     "QPushButton{border-radius: 115px}"
                                     "QPushButton{color: #FFFFFF}")
        
    def LoginClicked(self):
        self.ULELbl.move(9999,9999)
        self.PLELbl.move(9999,9999)
        found = False
        # Search in "teachers"
        users_ref = db.collection(u'teachers')
        users = users_ref.get()
        for user in users:
            if self.userLE.text()==user.to_dict()['username']:
                found = True
                # Check password
                if self.passLE.text()== user.to_dict()['password']:
                    # TODO - Change to TeacherProfile()
                    self.nd = StudentProfile()
                    self.nd.show()
                    self.hide()
                    break
                else:
                    self.ULELbl.move(9999,9999)
                    self.PLELbl.move(self.left+110,240+self.top)
                    self.passLE.setText("")

        # Serach in "students"
        if not found:
            users_ref = db.collection(u'students')
            users = users_ref.get()
            for user in users:
                if self.userLE.text()==user.to_dict()['username']:
                    found = True
                    # Check password
                    if self.passLE.text()== user.to_dict()['password']:
                        self.nd = StudentProfile()
                        self.nd.show()
                        self.hide()
                        break
                    else:
                        self.ULELbl.move(9999,9999)
                        self.PLELbl.move(self.left+110,240+self.top)
                        self.passLE.setText("")
                        

        # Not found in either "teachers" or "students"
        if not found:
            self.ULELbl.move(self.left+110,200+self.top)
            self.PLELbl.move(9999,9999)
            self.userLE.setText("")
            self.passLE.setText("")

    def SignUpClicked(self):
        if self.CheckUsername(self.userLE.text()) and self.CheckPassword(self.passLE.text()):
            users_ref = db.collection(u'teachers')
            users = users_ref.get()
            userID = ""

            found = False
            # Search in "teachers"
            for user in users:
                if self.userLE.text()==user.to_dict()['username']:
                    found = True
                    userID = user.id
                    break

            if found:
                doc_ref = db.collection(u'teachers').document(userID).set({
                    u'username': self.userLE.text(),
                    u'password': self.passLE.text()
                })
                
                confirmMB = QMessageBox.question(self, 'Successful', "Sign up successful", QMessageBox.Ok)
                # TODO - Change to TeacherProfile() later
                self.nd = StudentProfile()
                self.nd.show()
                self.hide()
            else:
                users_ref = db.collection(u'students')
                users = users_ref.get()
                
                # Search in "stdents"
                for user in users:
                    if self.userLE.text()==user.to_dict()['username']:
                        found = True
                        userID = user.id
                        break
                if found:        
                    doc_ref = db.collection(u'students').document(userID).set({
                        u'username': self.userLE.text(),
                        u'password': self.passLE.text()
                    })
                    confirmMB = QMessageBox.question(self, 'Successful', "Sign up successful", QMessageBox.Ok)
                    self.nd = StudentProfile()
                    self.nd.show()
                    self.hide()
                else:
                    errorMB = QMessageBox.question(self, 'Invalid', "Your ID is not found in the database", QMessageBox.Ok)
                    self.userLE.setText("")
                    self.passLE.setText("")

        else:
            if not self.CheckUsername(self.userLE.text()):
                errorMessageU = "1. Username must be your student ID(10 digits)\n"
                errorMB = QMessageBox.question(self, 'Invalid', errorMessageU, QMessageBox.Ok)
                self.userLE.setText("")
            else:
                errorMessageP1 = "1. Password length must be at least 6\n"
                errorMessageP2 = "2. Password must contain both numbers and alphabets\n"
                errorMessageP3 = "3. Password must contain both UPPERCASE and lowercase"
                errorMessage = errorMessageP1+errorMessageP2+errorMessageP3
                errorMB = QMessageBox.question(self, 'Invalid', errorMessage, QMessageBox.Ok)
                self.passLE.setText("")

    def ReadClicked(self):
        users_ref = db.collection(u'users')
        users = users_ref.get()

        for user in users:
            self.usersDict[user.to_dict()['username']] = user.to_dict()['password']
            #print(u'{} => {} : {}'.format(user.id, user.to_dict()['username'], user.to_dict()['password']))

        print()
        for key, value in self.usersDict.items():
            print(key, "\t\t:\t",value)

    def SignUpTabClicked(self):
        self.SignUpTab.setStyleSheet("QPushButton{background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FBC2EB,stop: 1 #A6C1EE)}"
                                    "QPushButton{border-radius: 115px;}"
                                    "QPushButton{color: #FFFFFF}")
        self.LoginTab.setStyleSheet("QPushButton{background-color: white}"
                                    "QPushButton{border-radius: 115px}"
                                    "QPushButton{color: #8e838e}")
        self.loginBtn.move(9999,9999)
        self.signupBtn.move(self.left-100, 280+self.top)
        self.tab = "signup"

    def LoginTabClicked(self):
        self.LoginTab.setStyleSheet("QPushButton{background-color: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #FBC2EB,stop: 1 #A6C1EE)}"
                                    "QPushButton{border-radius: 115px}"
                                    "QPushButton{color: #FFFFFF}")
        self.SignUpTab.setStyleSheet("QPushButton{background-color: white}"
                                    "QPushButton{border-radius: 115px}"
                                    "QPushButton{color: #8e838e}")
        self.signupBtn.move(9999,9999)
        self.loginBtn.move(self.left-100, 280+self.top)
        self.tab = "login"
    
    def CheckUsername(self, user):
        valid = True
        if not len(user)==10:
            valid = False
            print("Username length not equal to 10")
        if any(c.isalpha() for c in user):
            valid = False
            print("Found character")
        return valid

    def CheckPassword(self, passw):
        valid = True
        if len(passw) < 6:
            valid = False
            print("Password length is less than 6")
        if not (any(c.isalpha() for  c in passw) and any(c.isdigit() for c in passw)):
            valid = False
            print("Password must contain both alphabets and numbers")
        if not any(c.isupper() for c in passw):
            valid = False
            print("Password must contains at least one uppercase alphabet")
        if not any(c.islower() for c in passw):
            valid = False
        print(f"valid: {valid}")
        return valid

    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Return:
            if(self.tab == "signup"):
                self.SignUpClicked()
            else:
                self.LoginClicked()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = Login()
    sys.exit(app.exec_())