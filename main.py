import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def WaitForClass_CanBeClicked(driver, delaySec, class_name):
    wait = WebDriverWait(driver, delaySec)
    element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))

def WaitForClass_Visible(driver, delaySec, class_name):
    wait = WebDriverWait(driver, delaySec)
    wait.until(EC.visibility_of_element_located((By.CLASS_NAME, class_name)))

def WaitForTag_Visible(driver, delaySec, tag_name):
    wait = WebDriverWait(driver, delaySec)
    wait.until(EC.visibility_of_element_located((By.TAG_NAME, tag_name)))


def Login(self, driver, id, password):
    NewSleep(self, driver, 1)
    try:
        driver.get('https://myclass.ssu.ac.kr/login.php')

        #ID, PW 필드 채우기
        driver.fin
        driver.find_element_by_xpath('//*[@id="input-username"]').send_keys(id)
        driver.find_element_by_xpath('//*[@id="input-password"]').send_keys(password)

        #로그인 버튼 클릭
        driver.find_element_by_xpath('//*[@id="region-main"]/div/div/div/div[3]/div[1]/div[2]/form/div[2]/input').click()

        self.signal_AddLogMessage.emit("스마트캠퍼스에 로그인합니다..")
    except:
        self.signal_AddLogMessage.emit("웹페이지 로그인 실패, 서버에 문제가 발생했습니다")
        return


def mainFunc(self):
    user_id = self.id
    user_pw = self.pw