from selenium import webdriver
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi

import crf_main


class StartThread(QThread, QObject):                     #Threading setting
    #siganl definition
    signal_AddLogMessage = pyqtSignal(str)
    signal_StopFunction = pyqtSignal()

    def __init__(self, parent):
        super().__init__()

        self.main = parent

        self.isRun = False
        self.id = None
        self.pw = None
        self.date_selected = None
        self.refreshTime = 180
        self.midnightCheck = False
    
    def InitUserData(self, user_id, user_pw):
        self.id = user_id
        self.pw = user_pw
    
    def InitRefreshTime(self, refresh_time):
        self.refreshTime = refresh_time
    
    def InitDate(self, date_selected):
        self.date_selected = date_selected

    def InitCheck(self, state):
        self.midnightCheck = state

    def run(self):
        crf_main.mainFunc(self)
    def stop(self):
        # crf_main.mainFunc().stopFunc()
        self.terminate()



class Login(QDialog): 
    def __init__(self):
        super().__init__()

        #Thread
        self.th = StartThread(self)
        self.th.signal_AddLogMessage.connect(self.AddLogMessage)
        self.th.signal_StopFunction.connect(self.StopFunction)
        
        #UI 연결
        loadUi('login.ui', self)
        self.loginButton.clicked.connect(self.Loginfunction)
        self.logClearButton.clicked.connect(self.ClearLog)
        self.runButton.clicked.connect(self.RunFunction)
        self.stopButton.clicked.connect(self.StopFunction)
        


    def Loginfunction(self):
        id= self.idInput.text()
        pw= self.pwInput.text()
        
        if not id or not pw:
            self.AddLogMessage('ID, PW를 입력해주세요.')
        else:
            self.th.InitUserData(id, pw)    #id, pw저장
            self.AddLogMessage('로그인 정보 저장완료')

    def SetRefreshTime(self):
        refresh_time = self.refreshTimeInput.text()
        if not refresh_time:
            self.AddLogMessage('새로고침 시간이 기본(180초)으로 설정되었습니다.')
            self.th.InitRefreshTime(180)
        else:
            self.AddLogMessage('새로고침 시간이 '+refresh_time+'초로 설정되었습니다.')
            self.th.InitRefreshTime(refresh_time)

    def ClearLog(self):
        self.logBox.clear()
        self.AddLogMessage('로그 청소 완료.')

    def AddLogMessage(self, text):
        self.logBox.append(text)

    def RunFunction(self):
        if not self.th.isRun:
            refresh_time = self.refreshTimeInput.text()
            date_selected = self.dateSelectInput.text()
            if not date_selected:
                self.AddLogMessage('지정 날짜가 없습니다. 전체 검색을 시작합니다.')
            else:
                self.AddLogMessage('지정 날짜가 설정되었습니다 : '+date_selected)
                self.th.InitDate(date_selected)
            if not refresh_time:
                self.AddLogMessage('새로고침 시간이 기본(180초)으로 설정되었습니다.')
                self.th.InitRefreshTime(180)
            else:
                self.AddLogMessage('새로고침 시간이 '+refresh_time+'초로 설정되었습니다.')
                self.th.InitRefreshTime(refresh_time)
            self.th.isRun = True
            self.th.start()
            self.runButton.setDisabled(True)
            self.stopButton.setDisabled(False)
            self.loginButton.setDisabled(True)
            self.AddLogMessage('프로그램 실행..')

    def StopFunction(self):
         if self.th.isRun:
            self.th.isRun = False
            self.th.stop()
            self.stopButton.setDisabled(True)
            self.runButton.setDisabled(False)
            self.loginButton.setDisabled(False)
            self.AddLogMessage('프로그램 종료.')
            

if __name__ == "__main__":
    app=QApplication(sys.argv)
    mainWindow=Login()
    mainWindow.setFixedWidth(837)
    mainWindow.setFixedHeight(518)
    mainWindow.show()
    app.exec_()

