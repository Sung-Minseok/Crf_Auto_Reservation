import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver


import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QDialog
from PyQt5.QtCore import Qt, QThread
from PyQt5.uic import loadUi


url = 'https://crf.cau.ac.kr/2016/pages/reservation/view.php?eNum=35&searchCampus=1'
login_url = 'https://crf.cau.ac.kr/2016/pages/etc/login_pro.php'

loginData = {
    'memberId': '',
    'memberPwd': ''
}
response = requests.get(login_url,params=loginData)
print('로그인')
print(response.status_code)

def loginCheck(text):
    if text == None:
        return True
    else:
        return False


html = response.text
soup = bs(html, 'html.parser')

print(soup.select_one('#idBtnLogin'))


if response.status_code==200:
    print('='*30)
    print('success!!!')
else:
    print('='*30)
    print('status_code : ',response.status_code)


class StartThread(QThread):
    signal_AddLogMessage = pyqtSignal(str)
    
    def __init__(self, parent):
        super().__init__()

        self.main = parent
        self.id = None
        self.pw = None
    
    def InitUserData(self, user_id, user_pw):
        self.id = user_id
        self.pw = user_pw
    
    def run(self):
        mainFunc(self)



class Login(QDialog): 
    def __init__(self):
        super().__init__()

        #Thread
        self.th = StartThread(self)
        self.th.signal_AddLogMessage.connect(self.AddLogMessage)
        
        #UI 연결
        loadUi('login.ui', self)
        self.loginButton.clicked.connect(self.Loginfunction)
        self.logClearButton.clicked.connect(self.ClearLog)


    def Loginfunction(self):
        id= self.idInput.text()
        pw= self.pwInput.text()
        
        if not id or not pw:
            self.AddLogMessage('ID, PW를 입력해주세요.')
        else:
            loginData['memberId'] = id
            loginData['memberPwd'] = pw
            self.th.InitUserData(id, pw)    #id, pw저장
            self.AddLogMessage(id,'님 로그인 성공')
            print(soup.select_one('#idBtnLogin'))
            isLogin = loginCheck(soup.select_one('#idBtnLogin'))
            print(isLogin)
        print('id: ',id,'---pw : ',pw)

    def ClearLog(self):
        self.logBox.clear()
        self.AddLogMessage('로그 청소 완료.')

    def AddLogMessage(self, text):
        self.logBox.append(text)




app=QApplication(sys.argv)
mainWindow=Login()
widget=QtWidgets.QStackedWidget()
widget.addWidget(mainWindow)
widget.setFixedWidth(837)
widget.setFixedHeight(518)
widget.show()
app.exec_()

