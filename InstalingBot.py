from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import GetDictionary
import GetUsers
import FileIntegrityChecker

FileIntegrityChecker.checkFiles()
dictionary = GetDictionary.GetDictionary("slownik.txt")
users = GetUsers.GetUsers('Users.txt')

i = 1
while i < len(users)+1:
    service = Service(executable_path='C:\Program Files (x86)\chromedriver.exe')
    driver = webdriver.Chrome(service=service)

    driver.get("https://instaling.pl/teacher.php?page=login")

    Login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="log_email"]')))
    Login = driver.find_element_by_xpath('//*[@id="log_email"]')
    Login.send_keys(users[str(i)][1])#JA

    Password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="log_password"]')))
    Password = driver.find_element_by_xpath('//*[@id="log_password"]')
    Password.send_keys(users[str(i)][2])#JA
    Password.send_keys(Keys.RETURN)

    driver.get("https://instaling.pl/student/pages/mainPage.php?student_id="+users[str(i)][0]+"")#Ja

    Start_session = driver.find_element_by_xpath('//*[@id="student_panel"]/p[1]/a').click()
    sesja_przerwana = driver.find_element_by_xpath('//*[@id="continue_session_button"]').click()

    time.sleep(0.3)
    word = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="question"]/div[2]/div[2]')))
    word = driver.find_element_by_xpath('//*[@id="question"]/div[2]/div[2]').text

    while word != "Gratulacje!":
        time.sleep(0.5)
        word = driver.find_element_by_xpath('//*[@id="question"]/div[2]/div[2]').text
        usage_example = driver.find_element_by_xpath('//*[@id="question"]/div[1]').text

        if usage_example not in dictionary:
            try:
                Do_not_know = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dont_know_new"]')))
                Do_not_know = driver.find_element_by_xpath('//*[@id="dont_know_new"]').click()
                Skip_question = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="skip"]')))
                Skip_question = driver.find_element_by_xpath('//*[@id="skip"]').click()
            except ElementNotInteractableException:

                Answer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="answer"]')))
                Answer = driver.find_element_by_xpath('//*[@id="answer"]')
                Answer.send_keys("a")

                AnswerCheck = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="check"]/h4')))
                AnswerCheck = driver.find_element_by_xpath('//*[@id="check"]/h4').click()

                Translation = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="word"]')))
                Translation = driver.find_element_by_xpath('//*[@id="word"]').text

                try:
                    Next_question = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="nextword"]')))
                    Next_question.click()
                except ElementNotInteractableException as e:
                        print(f"Error clicking 'Next Question': {e}")

                file = open("slownik.txt", "a", encoding='utf-8')  
                file.write(usage_example,"|",word,"|",Translation,"\n")
                file.close()
                dictionary = GetDictionary.GetDictionary("slownik.txt")

        else:
            if usage_example in dictionary.keys():

                    Answer = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="answer"]')))
                    Answer = driver.find_element_by_xpath('//*[@id="answer"]')

                    Answer.send_keys(dictionary[usage_example])
                    AnswerCheck = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="check"]/h4')))
                    AnswerCheck = driver.find_element_by_xpath('//*[@id="check"]/h4').click()

                    try:
                        Next_question = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="nextword"]')))
                        Next_question.click()
                    except ElementNotInteractableException as e:
                        print(f"Error clicking 'Next Question': {e}")
                    time.sleep(0.5)
        test_word = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="summary"]/table/caption')))            
        test_word = driver.find_element_by_xpath('//*[@id="summary"]/table/caption').text
        if test_word == "Gratulacje!":
            word = test_word
        else:
            word = word
    time.sleep(0.5)
    Back_to_homepage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="return_mainpage"]')))
    Back_to_homepage = driver.find_element_by_xpath('//*[@id="return_mainpage"]').click()
    i=i+1
    driver.quit()
