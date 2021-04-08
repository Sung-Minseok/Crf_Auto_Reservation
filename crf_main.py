import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException




def Login(self, driver, id, pw):
    try:
        driver.get('https://crf.cau.ac.kr/2016/pages/reservation/view.php?eNum=35&searchCampus=1')

        #로그인 팝업 버튼 클릭
        driver.find_element_by_class_name('login_popup_open').click()
        
        #ID, PW 필드 채우기
        driver.find_element_by_id('memberId').send_keys(id)
        driver.find_element_by_id('memberPwd').send_keys(pw)

        #로그인 버튼 클릭
        driver.find_element_by_class_name('btn_login').click()

        popup = Alert(driver)
        if '오류' in popup.text:
            self.signal_AddLogMessage.emit(popup.text)
            popup.accept()
            driver.quit()
            self.signal_StopFunction.emit()
        else:
            popup.accept()
            self.signal_AddLogMessage.emit("로그인 완료.")
            driver.find_element_by_xpath('//*[@id="main_contents"]/div/div[3]/div[1]/div[1]/div[2]/div[1]/ul/li[3]/a/div[4]').click()   #장비선택
            driver.find_element_by_xpath('/html/body/div[3]/div/div/div[2]/a').click()  #예약하기버튼
            driver.switch_to_window(driver.window_handles[-1])  #새창으로 드라이버 변경
            time.sleep(3)
            
    except:
        driver.quit()
        self.signal_StopFunction.emit()
        return

def SelectDate(self,driver):
    try: 
        date = None
        _time = None
        _time_next = None
        nbspCheck = None
        holyDayCheck = None
        today_og = datetime.datetime.now()
        today = today_og.strftime('%m.%d')[1:]
        self.signal_AddLogMessage.emit(today)
        self.signal_AddLogMessage.emit('신청가능 시간 검색중...')

        for i in range(2,5):        #달력에서 세로줄(1주차~3주차)
            for j in range(1,8):    #달력에서 가로줄(일1~토7)
                #공휴일, 예약불가일 넘김
                if j == 1 or j == 7:
                    continue
                holyDayCheck = driver.find_element_by_xpath('//*[@id="calendar_month"]/table/tbody/tr/td/table[1]/tbody/tr['+str(i)+']/td['+str(j)+']').text  #날짜칸이 빈칸?
                if holyDayCheck =='' or holyDayCheck == ' ' or '예약불가' in holyDayCheck:
                    continue


                date_button= driver.find_element_by_xpath('//*[@id="calendar_month"]/table/tbody/tr/td/table[1]/tbody/tr['+str(i)+']/td['+str(j)+']/table/tbody/tr[1]/td/a')    #날짜
                date = date_button.text 
                #당일, 비어있는 날짜 넘김
                if date==today or date==' ':
                    continue
                dateIdx = 2
                _time_next = driver.find_element_by_xpath('//*[@id="calendar_month"]/table/tbody/tr/td/table[1]/tbody/tr['+str(i)+']/td['+str(j)+']/table/tbody/tr['+str(dateIdx)+']/td/span').text
                
                #해당 날짜 시간 끝날때까지 반복
                while True:
                    dateIdx += 1
                    _time_last = driver.find_element_by_xpath('//*[@id="calendar_month"]/table/tbody/tr/td/table[1]/tbody/tr['+str(i)+']/td['+str(j)+']/table/tbody/tr['+str(dateIdx)+']/td').text
                    if _time_last == ' ':
                        break
                    _time = _time_next
                    _time_next = driver.find_element_by_xpath('//*[@id="calendar_month"]/table/tbody/tr/td/table[1]/tbody/tr['+str(i)+']/td['+str(j)+']/table/tbody/tr['+str(dateIdx)+']/td/span').text
                    # self.signal_AddLogMessage.emit('time_next : '+ str(_time_next))
                    # self.signal_AddLogMessage.emit('time : '+str(_time))
                    sDate = _time[8:]
                    eDate = _time_next[:5]
                    if sDate != eDate:
                        self.signal_AddLogMessage.emit('신청가능 시간대 발견, 날짜 선택중..')
                        self.signal_AddLogMessage.emit('시간 : '+sDate+' ~ '+eDate)
                        
                        if sDate[0] == '0':             #시작, 종료 시간 세팅
                            sDate = sDate[1:]
                        if eDate[0] == '0':
                            eDate = eDate[1:]
                        sDate_1 = sDate.split(":")[0]
                        sDate_2 = sDate.split(":")[1]
                        if sDate_2 == '00':
                            sDate_2 = '0'
                        eDate_1 = eDate.split(":")[0]
                        eDate_2 = eDate.split(":")[1]
                        if eDate_2 == '00':
                            eDate_2 = '0'

                        if int(sDate_1) >= 18 : #18시 이상인지 체크
                            self.signal_AddLogMessage.emit('18시 이후 수업입니다. 권한 없음')
                            continue
                        if int(eDate_1) > 18:
                            eData_1 = '18'
                            eDate_2 = '0'

                        date_button.click() #날짜 선택
                        self.signal_AddLogMessage.emit('시간 선택중..')                    
                        driver.find_element_by_xpath('//*[@id="reserveSdate2"]/option[text()='+str(sDate_1)+']').click() #시작, 끝 시간 선택
                        driver.find_element_by_xpath('//*[@id="reserveSdate3"]/option[text()='+str(sDate_2)+']').click()
                        driver.find_element_by_xpath('//*[@id="reserveEdate2"]/option[text()='+str(eDate_1)+']').click()
                        driver.find_element_by_xpath('//*[@id="reserveEdate3"]/option[text()='+str(eDate_2)+']').click()
                        driver.find_element_by_xpath('//*[@id="isDirect"]').click() #직접사용 체크

                        self.signal_AddLogMessage.emit('신청버튼 클릭..')
                        driver.find_element_by_xpath('//*[@id="calendar_month"]/table/tbody/tr/td/div[9]/a[1]').click() #사용신청 클릭
                        popup2 = Alert(driver)  #팝업 처리
                        popup2.accept()
                        time.sleep(3)
                        popup3 = Alert(driver)
                        self.signal_AddLogMessage.emit(popup3.text)
                        popup3.accept()
                    
    except:
        driver.quit()
        self.signal_StopFunction.emit()
        return
                    

                

def mainFunc(self):
    user_id = self.id
    user_pw = self.pw

    #드라이버 로드
    try: 
        driver = webdriver.Chrome('chromedriver/chromedriver')
    except:
        self.signal_AddLogMessage.emit('크롬 드라이버 로딩 실패. 설치된 크롬 버전을 확인해주세요(최신 버전), chromedirver.exe가 폴더내에 존재하는지 확인해주세요.')
        return

    #로그인
    try:
        Login(self, driver, user_id, user_pw)
        user_id = None
        user_pw = None
    except:
        self.signal_AddLogMessage.emit('로그인에 실패하였습니다.')
        return

    #예약
    try:
        while True:
            SelectDate(self,driver)
            time.sleep(3)
            driver.refresh()
            time.sleep(int(self.refreshTime))
    except:
        self.signal_AddLogMessage.emit('문제가 발생했습니다, 프로그램 종료.')
        driver.quit()
        return
    self.signal_AddLogMessage.emit('시스템을 종료합니다.')
    driver.quit()
    